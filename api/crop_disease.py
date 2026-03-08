"""
MANDIMITRA — Crop Disease Detection API
========================================
POST /api/crop-disease/analyze   Upload crop image → Gemini Vision classification + advice
GET  /api/crop-disease/classes   List supported crops and diseases
"""

import base64
import io
import json
import logging
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastapi import APIRouter, File, Header, HTTPException, UploadFile
from PIL import Image

load_dotenv()

logger = logging.getLogger("mandimitra-api")

router = APIRouter(prefix="/api/crop-disease", tags=["Crop Disease Detection"])

# ============================================================================
# DISEASE KNOWLEDGE BASE (medicines, soil minerals, prevention)
# ============================================================================

_disease_kb = None
_KB_PATH = Path(__file__).resolve().parent.parent / "configs" / "disease_knowledge_base.json"


def _load_knowledge_base():
    """Load the disease treatment knowledge base (once)."""
    global _disease_kb
    if _disease_kb is not None:
        return
    if _KB_PATH.exists():
        with open(_KB_PATH, encoding="utf-8") as f:
            _disease_kb = json.load(f)
        logger.info(f"Disease knowledge base loaded: {len(_disease_kb) - 1} entries")
    else:
        logger.warning(f"Disease knowledge base not found at {_KB_PATH}")
        _disease_kb = {}


def _get_disease_treatment(predicted_class: str) -> dict | None:
    """Get treatment info (medicines, soil minerals) for a predicted class."""
    _load_knowledge_base()
    entry = _disease_kb.get(predicted_class)
    if not entry or predicted_class == "_meta":
        return None
    return {
        "disease_name_en": entry.get("disease_name_en"),
        "disease_name_mr": entry.get("disease_name_mr"),
        "pathogen": entry.get("pathogen"),
        "severity": entry.get("severity"),
        "summary_mr": entry.get("summary_mr"),
        "medicines": entry.get("medicines"),
        "soil_minerals": entry.get("soil_minerals"),
    }


def _build_advice_from_kb(predicted_class: str) -> dict:
    """Build an advice response from the knowledge base (no Gemini needed)."""
    _load_knowledge_base()
    entry = _disease_kb.get(predicted_class, {})
    crop, disease = _parse_class_name(predicted_class)
    is_healthy = "healthy" in disease.lower()

    if is_healthy:
        summary_mr = entry.get("summary_mr", f"तुमचे {entry.get('crop_mr', crop)} पीक निरोगी दिसत आहे.")
        return {
            "status": "healthy",
            "summary": entry.get("summary_en", f"Your {crop} crop appears healthy."),
            "description": summary_mr,
            "preventive_tips": entry.get("medicines", {}).get("prevention_mr", [
                "नियमित पाणी आणि खत व्यवस्थापन सुरू ठेवा",
                "पानांचा रंग आणि पोत यातील बदलांवर लक्ष ठेवा",
                "हवा खेळती राहण्यासाठी झाडांमध्ये योग्य अंतर ठेवा",
            ]),
            "recommended_actions": entry.get("medicines", {}).get("prevention", [
                "Continue current farming practices",
                "Monitor regularly for disease symptoms",
            ]),
        }

    # Diseased — build rich advice from KB
    display_disease = disease.replace("_", " ")
    disease_mr = entry.get("disease_name_mr", display_disease)
    pathogen = entry.get("pathogen", "")
    severity = entry.get("severity", "Moderate")
    summary_en = entry.get("summary_en", f"{display_disease} detected in {crop}.")
    summary_mr = entry.get("summary_mr", f"{disease_mr} आढळला.")

    # Build treatment list from medicines
    treatments = []
    medicines = entry.get("medicines", {})
    for t in medicines.get("treatments", []):
        treatments.append({
            "method": t.get("type", "Chemical"),
            "name": f"{t.get('name', '')} ({t.get('name_mr', '')})",
            "details": f"{t.get('application_mr', t.get('application', ''))} - मात्रा: {t.get('dosage_mr', t.get('dosage', ''))}"
        })

    # Build symptom list from summary
    symptoms = [summary_mr]

    # Prevention tips in Marathi
    prevention_mr = medicines.get("prevention_mr", medicines.get("prevention", []))

    return {
        "status": "diseased",
        "disease_name": display_disease,
        "summary": summary_en,
        "description": summary_mr,
        "causes": f"कारक: {pathogen}" if pathogen else None,
        "symptoms": symptoms,
        "treatment": treatments,
        "preventive_tips": prevention_mr,
        "severity": severity.lower() if severity else "moderate",
        "recommended_actions": medicines.get("prevention", [
            "Consult nearest agricultural extension office",
            "Apply recommended fungicides promptly",
        ]),
    }

# ============================================================================
# CLASS NAMES (17 classes from trained MobileNetV2 model)
# ============================================================================

_CLASS_NAMES = [
    "Corn___Common_Rust",
    "Corn___Gray_Leaf_Spot",
    "Corn___Healthy",
    "Corn___Northern_Leaf_Blight",
    "Potato___Early_Blight",
    "Potato___Healthy",
    "Potato___Late_Blight",
    "Rice___Brown_Spot",
    "Rice___Healthy",
    "Rice___Leaf_Blast",
    "Rice___Neck_Blast",
    "Sugarcane_Bacterial Blight",
    "Sugarcane_Healthy",
    "Sugarcane_Red Rot",
    "Wheat___Brown_Rust",
    "Wheat___Healthy",
    "Wheat___Yellow_Rust",
]

_MODEL_ACCURACY = 93.5  # Reported accuracy of the trained model


# ============================================================================
# CLASS NAME PARSING
# ============================================================================

# Known crops in the dataset
_KNOWN_CROPS = {"Corn", "Potato", "Rice", "Sugarcane", "Wheat"}


def _parse_class_name(class_name: str) -> tuple[str, str]:
    """Parse 'Crop___Disease' or 'Crop_Disease' into (crop, disease)."""
    # Try triple-underscore separator first (most classes)
    if "___" in class_name:
        parts = class_name.split("___", 1)
        return parts[0], parts[1]
    # Fallback: match known crop prefixes for single-underscore classes (Sugarcane)
    for crop in _KNOWN_CROPS:
        if class_name.startswith(crop + "_") or class_name.startswith(crop + " "):
            disease = class_name[len(crop) + 1:]
            return crop, disease
    return class_name, "Unknown"


# ============================================================================
# GEMINI VISION API — Image Classification + Advice
# ============================================================================

# Models to try in order (vision-capable, cheapest first)
_MODELS_TO_TRY = [
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-2.0-flash-lite",
    "gemini-1.5-flash-8b",
]


def _get_api_keys() -> list[str]:
    """
    Load API keys from env. Supports multiple comma-separated keys for rotation.
    Env vars checked: GEMINI_API_KEYS (plural), GEMINI_API_KEY, Gemini_API_KEY.
    Example:  GEMINI_API_KEYS=AIza...aaa,AIza...bbb,AIza...ccc
    """
    raw = os.getenv("GEMINI_API_KEYS") or os.getenv("GEMINI_API_KEY") or os.getenv("Gemini_API_KEY") or ""
    keys = [k.strip() for k in raw.split(",") if k.strip()]
    return keys


_PROMPT_TEMPLATE: str | None = None


def _build_prompt() -> str:
    global _PROMPT_TEMPLATE
    if _PROMPT_TEMPLATE:
        return _PROMPT_TEMPLATE

    class_list = ", ".join(_CLASS_NAMES)
    _PROMPT_TEMPLATE = f"""You are an expert agricultural scientist and plant pathologist.

Analyze this crop leaf image and classify it into EXACTLY ONE of these classes:
{class_list}

Then provide disease advice.

Respond in this EXACT JSON format (no markdown fences):
{{
  "predicted_class": "exact class name from the list above",
  "confidence": 85.0,
  "top_predictions": [
    {{"class": "most likely class", "confidence": 85.0}},
    {{"class": "second most likely", "confidence": 10.0}},
    {{"class": "third most likely", "confidence": 5.0}}
  ],
  "advice": {{
    "status": "healthy or diseased",
    "summary": "One-line summary",
    "description": "Detailed description (3-4 sentences)",
    "disease_name": "Common name of disease (null if healthy)",
    "causes": "What causes this (null if healthy)",
    "symptoms": ["symptom1", "symptom2"],
    "treatment": [
      {{"method": "Chemical/Organic/Cultural", "name": "Treatment name", "details": "How to apply"}}
    ],
    "preventive_tips": ["tip1", "tip2", "tip3"],
    "severity": "mild/moderate/severe (null if healthy)",
    "recommended_actions": ["action1", "action2"]
  }}
}}

IMPORTANT: predicted_class MUST be exactly one of the listed classes. Confidence should reflect your certainty (0-100)."""
    return _PROMPT_TEMPLATE


def _analyze_with_gemini(image_bytes: bytes) -> dict:
    """
    Use Gemini Vision API to classify crop disease from image AND provide advice.
    Rotates through multiple API keys and model variants for resilience.
    """
    api_keys = _get_api_keys()
    if not api_keys:
        raise HTTPException(503, "Gemini API key not configured on server")

    from google import genai

    prompt = _build_prompt()

    # Encode image for Gemini
    img_b64 = base64.b64encode(image_bytes).decode("utf-8")

    # Detect mime type
    img = Image.open(io.BytesIO(image_bytes))
    fmt = img.format or "JPEG"
    mime_map = {"JPEG": "image/jpeg", "JPG": "image/jpeg", "PNG": "image/png", "WEBP": "image/webp"}
    mime_type = mime_map.get(fmt.upper(), "image/jpeg")

    contents = [
        {
            "role": "user",
            "parts": [
                {"inline_data": {"mime_type": mime_type, "data": img_b64}},
                {"text": prompt},
            ],
        }
    ]

    last_error = None

    # Try every key × every model combination
    for key_idx, api_key in enumerate(api_keys):
        client = genai.Client(api_key=api_key)
        for model_name in _MODELS_TO_TRY:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=contents,
                )

                text = response.text.strip()
                if text.startswith("```"):
                    text = text.split("\n", 1)[1]
                    if text.endswith("```"):
                        text = text[:-3]
                    text = text.strip()

                result = json.loads(text)

                # Validate predicted_class is in our list
                if result.get("predicted_class") not in _CLASS_NAMES:
                    pred = result.get("predicted_class", "")
                    for cls in _CLASS_NAMES:
                        if pred.lower().replace(" ", "_") == cls.lower().replace(" ", "_"):
                            result["predicted_class"] = cls
                            break
                    else:
                        logger.warning(f"Gemini returned unknown class: {pred}")

                logger.info(
                    f"Gemini Vision classified: {result.get('predicted_class')} "
                    f"using {model_name} (key #{key_idx + 1})"
                )
                return result

            except json.JSONDecodeError as e:
                logger.error(f"Gemini ({model_name}, key#{key_idx + 1}) returned non-JSON: {e}")
                last_error = e
                continue
            except Exception as e:
                err_str = str(e)
                last_error = e
                # If quota/rate-limit error, skip remaining models for this key
                if "RESOURCE_EXHAUSTED" in err_str or "429" in err_str:
                    logger.warning(f"Key #{key_idx + 1} quota exhausted, trying next key...")
                    break
                logger.warning(f"Gemini {model_name} (key#{key_idx + 1}) failed: {e}")
                continue

    raise HTTPException(
        503,
        "सर्व AI मॉडेल्स सध्या व्यस्त आहेत. कृपया 1 मिनिटानंतर पुन्हा प्रयत्न करा. "
        "/ All AI models are currently busy. Please try again in 1 minute.",
    )


# ============================================================================
# HELPER: AUTH
# ============================================================================

async def _require_user(authorization: Optional[str]) -> dict:
    """Validate token and return user profile."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Missing or invalid authorization header")

    token = authorization.replace("Bearer ", "")

    from api.auth import _decode_token, _get_profile

    payload = _decode_token(token)
    uid = payload.get("sub")
    profile = await _get_profile(uid)
    if not profile:
        raise HTTPException(401, "Invalid or expired token")
    return profile


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/analyze")
async def analyze_crop_disease(
    file: UploadFile = File(...),
    authorization: str = Header(None),
):
    """
    Upload a crop leaf image -> Gemini Vision classification + advice.
    Returns crop name, disease (or healthy), confidence, and detailed treatment guidance.
    """
    user = await _require_user(authorization)

    # Validate file type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(400, "Only image files (JPG, PNG) are accepted")

    # Read and validate size (max 10 MB)
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(400, "Image must be under 10 MB")

    # Classify with Gemini Vision API
    gemini_result = _analyze_with_gemini(content)

    predicted_class = gemini_result.get("predicted_class", _CLASS_NAMES[2])
    confidence = gemini_result.get("confidence", 0)
    top_predictions = gemini_result.get("top_predictions", [])
    advice = gemini_result.get("advice", {})

    # Parse crop and disease from class name
    crop, disease = _parse_class_name(predicted_class)
    is_healthy = "healthy" in disease.lower()

    logger.info(
        f"Crop disease analysis: {predicted_class} ({confidence}%) "
        f"for user {user.get('full_name', user['id'])}"
    )

    # Get structured treatment info from knowledge base
    treatment = _get_disease_treatment(predicted_class)

    result = {
        "crop": crop,
        "disease": disease.replace("_", " ") if not is_healthy else None,
        "is_healthy": is_healthy,
        "predicted_class": predicted_class,
        "confidence": round(confidence, 1),
        "top_predictions": top_predictions,
        "advice": advice,
        "model_accuracy": _MODEL_ACCURACY,
    }
    if treatment:
        result["treatment"] = treatment

    return result


@router.get("/classes")
async def get_supported_classes():
    """Return list of supported crops and their diseases."""
    crops = {}
    for cls in _CLASS_NAMES:
        crop, condition = _parse_class_name(cls)
        if crop not in crops:
            crops[crop] = []
        crops[crop].append(condition.replace("_", " "))

    return {
        "total_classes": len(_CLASS_NAMES),
        "crops": crops,
        "model_accuracy": _MODEL_ACCURACY,
    }


@router.get("/treatment/{disease_class}")
async def get_treatment_info(disease_class: str):
    """Return structured treatment info (medicines, soil minerals) for a disease class."""
    treatment = _get_disease_treatment(disease_class)
    if treatment is None:
        raise HTTPException(404, f"No treatment info for class '{disease_class}'")
    return treatment


@router.get("/kb-advice/{disease_class}")
async def get_kb_advice(disease_class: str):
    """Return structured advice built from the knowledge base (no Gemini needed)."""
    if disease_class not in _CLASS_NAMES:
        raise HTTPException(404, f"Unknown disease class: '{disease_class}'")
    return _build_advice_from_kb(disease_class)
