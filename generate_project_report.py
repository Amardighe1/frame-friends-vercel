"""
FarmFriend -- Capstone Project Report PDF Generator
"""
from fpdf import FPDF
import os

class Report(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(120, 120, 120)
            self.cell(0, 8, "FarmFriend - AI-Powered Agricultural Intelligence | Capstone Project Report", align="C")
            self.ln(4)
            self.set_draw_color(16, 185, 129)
            self.set_line_width(0.5)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def section_title(self, num, title):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(5, 100, 60)
        self.cell(0, 10, f"{num}. {title}", ln=True)
        self.set_draw_color(16, 185, 129)
        self.set_line_width(0.8)
        self.line(10, self.get_y(), 80, self.get_y())
        self.ln(4)

    def sub_title(self, title):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(30, 30, 30)
        self.cell(0, 8, title, ln=True)
        self.ln(1)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def bullet(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        x = self.get_x()
        self.cell(6, 5.5, "-")
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def bold_bullet(self, label, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        self.cell(6, 5.5, "-")
        self.set_font("Helvetica", "B", 10)
        self.write(5.5, f"{label}: ")
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def table(self, headers, rows, col_widths=None):
        if col_widths is None:
            col_widths = [190 / len(headers)] * len(headers)
        # Header row
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(16, 185, 129)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 7, h, border=1, fill=True, align="C")
        self.ln()
        # Data rows
        self.set_font("Helvetica", "", 9)
        self.set_text_color(40, 40, 40)
        fill = False
        for row in rows:
            if self.get_y() > 265:
                self.add_page()
            if fill:
                self.set_fill_color(240, 250, 245)
            else:
                self.set_fill_color(255, 255, 255)
            max_h = 7
            for i, val in enumerate(row):
                self.cell(col_widths[i], max_h, str(val), border=1, fill=True, align="C" if i > 0 else "L")
            self.ln()
            fill = not fill
        self.ln(3)


def build():
    pdf = Report()
    pdf.alias_nb_pages()

    # ===== COVER PAGE =====
    pdf.add_page()
    pdf.ln(30)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(5, 100, 60)
    pdf.cell(0, 15, "FarmFriend", align="C", ln=True)
    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 8, "AI-Powered Agricultural Intelligence", align="C", ln=True)
    pdf.cell(0, 8, "for Maharashtra Farmers", align="C", ln=True)
    pdf.ln(8)
    pdf.set_draw_color(16, 185, 129)
    pdf.set_line_width(1)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(12)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 7, "Final Year Diploma Capstone Project", align="C", ln=True)
    pdf.cell(0, 7, "Course Code: 316004", align="C", ln=True)
    pdf.ln(6)
    pdf.cell(0, 7, "Submitted by: Amar Dighe", align="C", ln=True)
    pdf.cell(0, 7, "Guide: [Faculty Name]", align="C", ln=True)
    pdf.ln(6)
    pdf.cell(0, 7, "Department of Computer Engineering", align="C", ln=True)
    pdf.cell(0, 7, "[College Name], Maharashtra", align="C", ln=True)
    pdf.ln(10)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(5, 100, 60)
    pdf.cell(0, 7, "Academic Year 2025-2026", align="C", ln=True)
    pdf.ln(20)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 6, "Version 2.1.0 | MIT License | March 2026", align="C", ln=True)

    # ===== 1. ABSTRACT =====
    pdf.add_page()
    pdf.section_title("1", "Abstract")
    pdf.body_text(
        "FarmFriend is a production-grade, AI-powered agricultural decision support system built for "
        "Maharashtra farmers. It transforms 3.5M+ government mandi records, satellite weather data, and "
        "crop disease imagery into actionable intelligence through three trained ML models -- Crop Risk "
        "Advisor (LightGBM, 87.4% accuracy), Price Intelligence Engine (LightGBM, R2=0.933), and Crop "
        "Disease Detector (MobileNetV2 CNN, 93.47% accuracy). The system features a FastAPI backend, "
        "Next.js 14 frontend, MongoDB database, and a Capacitor-based Android APK with Marathi-first UI. "
        "Key capabilities include real-time crop risk assessment, multi-horizon price forecasting with "
        "conformal prediction intervals, on-device crop disease detection with treatment recommendations, "
        "live mandi price tracking, veterinary emergency SOS with geo-based auto-assignment, and a buyer "
        "marketplace. Deployed on Vercel (frontend) and AWS EC2 (backend) with Docker containerization."
    )

    # ===== 2. INTRODUCTION =====
    pdf.section_title("2", "Introduction")
    pdf.sub_title("2.1 Problem Statement")
    pdf.body_text(
        "Maharashtra farmers face critical challenges: volatile commodity prices causing financial losses, "
        "crop diseases going undetected until severe damage, lack of accessible weather-based risk assessment, "
        "and limited access to veterinary emergency services in rural areas. Existing solutions are fragmented, "
        "English-only, and inaccessible to the average Marathi-speaking farmer."
    )
    pdf.sub_title("2.2 Proposed Solution")
    pdf.body_text(
        "FarmFriend provides an integrated, Marathi-first platform combining three ML models with real-time "
        "data from government APIs. Farmers can assess crop risk before sowing, forecast commodity prices "
        "with confidence intervals, detect crop diseases via phone camera, track live mandi prices, and "
        "request emergency veterinary help -- all in one application."
    )
    pdf.sub_title("2.3 Objectives")
    pdf.bullet("Build a data pipeline ingesting 3.5M+ mandi records from AGMARKNET + 10 years weather from NASA POWER")
    pdf.bullet("Train 3 ML models: Crop Risk (LightGBM), Price Forecast (LightGBM), Disease Detection (CNN)")
    pdf.bullet("Develop a FastAPI REST backend with 40+ endpoints and JWT authentication")
    pdf.bullet("Create a responsive Next.js web app + Android APK with Marathi-first UI")
    pdf.bullet("Implement veterinary emergency SOS with geo-based doctor auto-assignment")
    pdf.bullet("Deploy with Docker on AWS EC2 (backend) and Vercel (frontend)")

    # ===== 3. LITERATURE REVIEW / RESEARCH PAPERS =====
    pdf.add_page()
    pdf.section_title("3", "Literature Review & Research Papers Implemented")
    pdf.bold_bullet("MobileNetV2 (Sandler et al., 2018)",
                    "Inverted residuals with linear bottlenecks for efficient mobile CNN. Used as backbone for 17-class crop disease detection. ~14 MB model size.")
    pdf.bold_bullet("MT-CYP-Net (arXiv:2505.12069)",
                    "Multi-task crop yield prediction with focal-loss class weighting. Adopted focal-loss weights {Low:1, Medium:10, High:50} for crop risk model, improving High Risk Recall by +3.1%.")
    pdf.bold_bullet("NeuralCrop (arXiv:2512.20177)",
                    "Physics-informed neural features for crop modeling. Implemented GDD (Growing Degree Days), VPD (Vapor Pressure Deficit), and Drought Stress Index as engineered features.")
    pdf.bold_bullet("Conformal Prediction (Shafer & Vovk, 2005)",
                    "Distribution-free prediction intervals. Applied to price forecasting: 80% CI, 90% CI, and 95% CI bands calibrated on held-out data.")
    pdf.bold_bullet("LightGBM (Ke et al., 2017)",
                    "Gradient boosting with leaf-wise growth and histogram binning. Used for both crop risk classification and multi-horizon price regression.")

    # ===== 4. SYSTEM ARCHITECTURE =====
    pdf.section_title("4", "System Architecture")
    pdf.sub_title("4.1 Three-Tier Architecture")
    pdf.body_text(
        "Data Layer: AGMARKNET API (3.5M+ records), NASA POWER (10yr weather), Open-Meteo (16-day forecast), "
        "MongoDB Atlas (users, bookings, emergencies, buyer prices).\n\n"
        "ML/API Layer: FastAPI v2.1.0 on Docker (Python 3.10), LightGBM models (~24 MB), on-device TF.js CNN "
        "(saves ~400MB on server), JWT auth, Gemini AI integration.\n\n"
        "Presentation Layer: Next.js 14 (Vercel), Capacitor Android APK, Marathi-first bilingual UI, "
        "Leaflet maps, Recharts visualization."
    )
    pdf.sub_title("4.2 Deployment Architecture")
    pdf.body_text(
        "Frontend: Next.js on Vercel (auto-deploy on git push) with API rewrites to backend.\n"
        "Backend: FastAPI in Docker container on AWS EC2 (t3.micro), port 8000.\n"
        "Database: MongoDB Atlas (cloud). External APIs: Data.gov.in, Open-Meteo, Gemini AI.\n"
        "Mobile: Capacitor APK loads UI from Vercel URL -> auto-updates without re-installing APK."
    )

    # ===== 5. TECHNOLOGY STACK =====
    pdf.add_page()
    pdf.section_title("5", "Technology Stack")
    pdf.sub_title("5.1 Frontend")
    pdf.table(
        ["Technology", "Version", "Purpose"],
        [
            ["Next.js", "14.2.0", "React framework (SSR + static)"],
            ["React + TypeScript", "18.2 / 5.3", "UI + type safety"],
            ["Tailwind CSS", "3.4.1", "Utility-first styling"],
            ["TensorFlow.js", "4.22.0", "On-device crop disease CNN"],
            ["Capacitor", "8.1.0", "Native Android APK"],
            ["Framer Motion", "11.0.8", "Animations"],
            ["Recharts", "2.12.2", "Data visualization"],
            ["Leaflet", "1.9.4", "Interactive maps"],
            ["Radix UI", "Multiple", "Accessible UI primitives"],
        ],
        [60, 30, 100]
    )
    pdf.sub_title("5.2 Backend")
    pdf.table(
        ["Technology", "Version", "Purpose"],
        [
            ["Python", "3.10+", "Core language"],
            ["FastAPI", "0.104+", "REST API framework"],
            ["LightGBM", "4.0+", "Crop Risk + Price models"],
            ["scikit-learn", "1.3+", "ML preprocessing"],
            ["MongoDB (Motor)", "3.3+", "Async database driver"],
            ["PyJWT + bcrypt", "2.8+ / 4.0+", "Auth & password hashing"],
            ["Gemini AI (genai)", "1.0+", "AI treatment advice"],
            ["Docker", "Python 3.10-slim", "Containerization"],
        ],
        [60, 30, 100]
    )

    # ===== 6. ML MODELS =====
    pdf.add_page()
    pdf.section_title("6", "Machine Learning Models")

    pdf.sub_title("6.1 Model 1: Crop Risk Advisor")
    pdf.bold_bullet("Algorithm", "LightGBM Classifier (gradient boosting)")
    pdf.bold_bullet("Training Data", "3.5M+ mandi records + 10yr weather data (36 districts)")
    pdf.bold_bullet("Classes", "Low Risk, Medium Risk, High Risk")
    pdf.bold_bullet("Accuracy", "87.4% (CV: 88.0%)")
    pdf.bold_bullet("F1 Macro", "61.08% (CV: 62.02%)")
    pdf.bold_bullet("High Risk Recall", "45.89% (+3.1% via focal-loss weights)")
    pdf.bold_bullet("Key Features", "GDD, VPD, Drought Stress Index, district, temp_std, stage_progress")
    pdf.bold_bullet("Physics Features", "From NeuralCrop paper -- biology-informed feature engineering")
    pdf.bold_bullet("Crops Supported", "Soybean, Cotton, Jowar, Bajra, Wheat, Gram, Groundnut, Tur, Maize, Rice, Sugarcane, Onion")
    pdf.ln(3)

    pdf.sub_title("6.2 Model 2: Price Intelligence Engine")
    pdf.bold_bullet("Algorithm", "Multi-horizon LightGBM Regressor (5 separate models)")
    pdf.bold_bullet("Horizons", "1-day, 3-day, 7-day, 14-day, 15-day")
    pdf.bold_bullet("Features", "60 features (lag, rolling stats, momentum, volatility, calendar, weather)")
    pdf.bold_bullet("Training Data", "3.29M records per horizon")
    pdf.bold_bullet("Prediction Intervals", "Conformal Prediction at 80%, 90%, 95% CI")
    pdf.table(
        ["Horizon", "MAE", "RMSE", "R2", "MAPE"],
        [
            ["1-day", "361.72", "687.77", "0.933", "21.3%"],
            ["3-day", "435.38", "803.34", "0.910", "26.2%"],
            ["7-day", "501.82", "896.52", "0.890", "34.6%"],
            ["14-day", "561.81", "983.83", "0.868", "47.6%"],
            ["15-day", "546.28", "924.92", "0.882", "44.8%"],
        ],
        [30, 35, 40, 40, 45]
    )

    pdf.sub_title("6.3 Model 3: Crop Disease Detector")
    pdf.bold_bullet("Architecture", "MobileNetV2 + custom classification head (transfer learning)")
    pdf.bold_bullet("Input", "224x224 RGB images")
    pdf.bold_bullet("Classes", "17 (5 crops x diseases + healthy states)")
    pdf.bold_bullet("Validation Accuracy", "93.47%")
    pdf.bold_bullet("Phase 1 (frozen)", "90.35% accuracy")
    pdf.bold_bullet("Phase 2 (fine-tuned)", "93.47% accuracy")
    pdf.bold_bullet("Model Size", "~14 MB (.keras format)")
    pdf.bold_bullet("Deployment", "On-device via TensorFlow.js (browser/APK) -- not on server")
    pdf.bold_bullet("Dataset", "13,324 images across 17 classes")
    pdf.ln(2)
    pdf.body_text("17 Classes: Corn (Common Rust, Gray Leaf Spot, Healthy, Northern Leaf Blight), "
                  "Potato (Early Blight, Healthy, Late Blight), Rice (Brown Spot, Healthy, Leaf Blast, Neck Blast), "
                  "Sugarcane (Bacterial Blight, Healthy, Red Rot), Wheat (Brown Rust, Healthy, Yellow Rust)")

    # ===== 7. FEATURES & MODULES =====
    pdf.add_page()
    pdf.section_title("7", "Features & Modules")

    pdf.sub_title("7.1 Crop Risk Assessment")
    pdf.body_text("Farmer selects crop, district, and sowing date. System fetches weather forecast and runs "
                  "the LightGBM model to predict risk level (Low/Medium/High) with confidence percentage.")

    pdf.sub_title("7.2 Price Forecasting")
    pdf.body_text("Select commodity and market. System runs 5 LightGBM models for 1-day to 15-day price "
                  "predictions with conformal 80/90/95% confidence intervals displayed on interactive charts.")

    pdf.sub_title("7.3 Crop Disease Detection")
    pdf.body_text("Upload crop leaf photo. MobileNetV2 CNN runs on-device (TF.js) for instant prediction. "
                  "Cloud fallback uses Gemini AI for detailed treatment advice. Knowledge base provides "
                  "medicines, fungicides with dosages, and soil mineral deficiency analysis -- all in Marathi.")

    pdf.sub_title("7.4 Live Mandi Prices")
    pdf.body_text("Real-time prices from AGMARKNET (Data.gov.in) with 24-hour auto-refresh. Filter by "
                  "commodity, market, district. Displays min/max/modal prices.")

    pdf.sub_title("7.5 Weather Forecast")
    pdf.body_text("16-day forecast via Open-Meteo API for all 36 Maharashtra districts. Interactive Leaflet "
                  "maps with temperature, rainfall, humidity data.")

    pdf.sub_title("7.6 Veterinary Emergency SOS")
    pdf.body_text("One-tap emergency request. System auto-assigns nearest verified vet doctor based on GPS "
                  "coordinates. Doctor can accept/reject (escalates to next nearest). Full booking management "
                  "with appointment scheduling.")

    pdf.sub_title("7.7 Buyer Marketplace")
    pdf.body_text("Buyers post daily crop prices. Farmers search by market and crop to find best prices. "
                  "14 crops supported with Marathi names. Auto-expiry of stale listings.")

    pdf.sub_title("7.8 Role-Based Access")
    pdf.table(
        ["Role", "Capabilities"],
        [
            ["Farmer", "Risk assessment, prices, disease scan, weather, vet booking, SOS"],
            ["Doctor", "Profile, emergencies, bookings, document upload, GPS update"],
            ["Buyer", "Post prices, manage listings, market selection"],
            ["Admin", "2-step login, verify doctors, dashboard stats"],
        ],
        [35, 155]
    )

    # ===== 8. API ENDPOINTS =====
    pdf.add_page()
    pdf.section_title("8", "API Endpoints (40+)")
    pdf.sub_title("Authentication (6 endpoints)")
    pdf.table(["Method", "Endpoint", "Description"],
              [["POST", "/api/auth/signup", "Register (farmer/doctor/buyer)"],
               ["POST", "/api/auth/login", "Login with JWT"],
               ["POST", "/api/auth/admin/verify", "Admin step 1: verify ID"],
               ["POST", "/api/auth/admin/login", "Admin step 2: credentials"],
               ["GET", "/api/auth/me", "Current user from token"],
               ["POST", "/api/auth/logout", "Logout"]],
              [20, 65, 105])

    pdf.sub_title("ML Prediction (6 endpoints)")
    pdf.table(["Method", "Endpoint", "Description"],
              [["POST", "/api/crop-risk/assess", "Crop risk LightGBM prediction"],
               ["GET", "/api/crop-risk/crops", "List supported crops"],
               ["GET", "/api/crop-risk/districts", "List districts"],
               ["POST", "/api/price/forecast", "Multi-horizon price forecast"],
               ["GET", "/api/price/commodities", "Top 30 commodities"],
               ["GET", "/api/price/markets", "Available markets"]],
              [20, 65, 105])

    pdf.sub_title("Crop Disease (3 endpoints)")
    pdf.table(["Method", "Endpoint", "Description"],
              [["POST", "/api/crop-disease/analyze", "Image upload -> CNN + Gemini advice"],
               ["GET", "/api/crop-disease/classes", "List 17 disease classes"],
               ["GET", "/api/crop-disease/treatment/{cls}", "Treatment knowledge base"]],
              [20, 75, 95])

    pdf.sub_title("Weather & Market (5 endpoints)")
    pdf.table(["Method", "Endpoint", "Description"],
              [["GET", "/api/weather/forecast", "16-day forecast (Open-Meteo)"],
               ["GET", "/api/weather/districts", "Districts with coordinates"],
               ["GET", "/api/market/prices", "Live mandi prices"],
               ["GET", "/api/market/commodities", "Commodities list"],
               ["GET", "/api/market/summary", "Market statistics"]],
              [20, 65, 105])

    pdf.sub_title("Veterinary (14 endpoints) & Buyer (6 endpoints)")
    pdf.body_text("Vet module: admin doctor verification, doctor profile/location/bookings/emergencies, "
                  "farmer booking/SOS creation. Buyer module: CRUD prices, market/crop lists, farmer search.")

    # ===== 9. DATA SOURCES =====
    pdf.add_page()
    pdf.section_title("9", "Data Sources")
    pdf.table(
        ["Source", "Data", "Volume"],
        [
            ["AGMARKNET (Data.gov.in)", "Daily mandi commodity prices", "3.5M+ records"],
            ["Kaggle Historical", "Multi-year mandi price archive", "Large dataset"],
            ["NASA POWER", "10yr daily weather (precip, temp, humidity)", "36 districts"],
            ["Open-Meteo", "16-day weather forecasts", "Real-time API"],
            ["Disease Knowledge Base", "Treatment info (IRRI, ICAR, FAO)", "17 classes"],
            ["Crop Lifecycle Config", "Growth stages, sowing windows, thresholds", "12+ crops"],
        ],
        [55, 80, 55]
    )

    # ===== 10. KEY STATISTICS =====
    pdf.section_title("10", "Key Statistics")
    pdf.table(
        ["Metric", "Value"],
        [
            ["Total mandi records processed", "3.5M+"],
            ["Maharashtra districts", "36"],
            ["Maharashtra mandis/markets", "300+"],
            ["Disease detection classes", "17"],
            ["Disease detection accuracy", "93.47%"],
            ["Crop risk accuracy", "87.4%"],
            ["Price model R2 (1-day)", "0.933"],
            ["Price model R2 (7-day)", "0.890"],
            ["Forecast horizons", "5 (1, 3, 7, 14, 15 days)"],
            ["ML features (price model)", "60"],
            ["Disease dataset images", "13,324"],
            ["Disease model size", "~14 MB"],
            ["API endpoints", "40+"],
            ["Crops (risk advisor)", "12+"],
            ["Crops (disease detection)", "5"],
            ["Buyer crops supported", "14 (bilingual)"],
            ["Weather forecast range", "16 days"],
            ["Historical weather", "10 years"],
            ["Confidence intervals", "80%, 90%, 95%"],
            ["Total development cost", "Rs.0 (open-source/free-tier)"],
        ],
        [100, 90]
    )

    # ===== 11. TESTING =====
    pdf.add_page()
    pdf.section_title("11", "Testing & Validation")
    pdf.sub_title("11.1 ML Model Validation")
    pdf.bullet("Crop Risk: 5-fold cross-validation, focal-loss tuned, stratified split")
    pdf.bullet("Price Model: Walk-forward validation (temporal split), conformal calibration on held-out set")
    pdf.bullet("Disease CNN: 80/20 train-val split, fine-tuning from ImageNet weights, per-class accuracy logged")

    pdf.sub_title("11.2 API Testing")
    pdf.bullet("All 40+ endpoints tested via FastAPI /docs (Swagger UI)")
    pdf.bullet("Auth flow tested: signup -> login -> JWT token -> protected endpoints")
    pdf.bullet("Error handling validated: malformed inputs, unauthorized access, missing data")

    pdf.sub_title("11.3 Frontend Testing")
    pdf.bullet("Responsive UI tested on mobile (360px) to desktop (1440px)")
    pdf.bullet("APK tested on physical Android device (Samsung, Xiaomi)")
    pdf.bullet("On-device TF.js inference tested in Capacitor WebView")

    # ===== 12. FUTURE SCOPE =====
    pdf.section_title("12", "Future Scope")
    pdf.bullet("Expand to all Indian states (currently Maharashtra only)")
    pdf.bullet("Add multi-language support (Hindi, Kannada, Telugu)")
    pdf.bullet("Integrate satellite imagery (NDVI) for field-level crop monitoring")
    pdf.bullet("SMS-based alerts for price changes and weather warnings")
    pdf.bullet("Implement ViT (Vision Transformer) for disease detection with larger dataset")
    pdf.bullet("Add offline-first capability with service workers for low-connectivity areas")
    pdf.bullet("Government subsidy information integration")

    # ===== 13. CONCLUSION =====
    pdf.section_title("13", "Conclusion")
    pdf.body_text(
        "FarmFriend successfully demonstrates that AI and ML can be applied to real agricultural problems "
        "at production scale. The system processes 3.5M+ government records, delivers 93.47% disease "
        "detection accuracy, and provides actionable price forecasts with R2=0.933. The Marathi-first "
        "approach ensures accessibility for the target user base. The three-model architecture (Risk + "
        "Price + Disease) provides comprehensive decision support covering the entire crop lifecycle -- "
        "from pre-sowing risk assessment to post-harvest price optimization. With zero development cost "
        "using open-source tools and free-tier cloud services, the project proves that impactful AgriTech "
        "solutions can be built and deployed affordably."
    )

    # ===== 14. REFERENCES =====
    pdf.add_page()
    pdf.section_title("14", "References")
    pdf.bullet("Sandler, M. et al. (2018). MobileNetV2: Inverted Residuals and Linear Bottlenecks. CVPR 2018.")
    pdf.bullet("Ke, G. et al. (2017). LightGBM: A Highly Efficient Gradient Boosting Decision Tree. NeurIPS 2017.")
    pdf.bullet("MT-CYP-Net (2025). Multi-task Crop Yield Prediction. arXiv:2505.12069.")
    pdf.bullet("NeuralCrop (2025). Physics-informed Neural Features for Crop Modeling. arXiv:2512.20177.")
    pdf.bullet("Shafer, G. & Vovk, V. (2005). A Tutorial on Conformal Prediction. JMLR.")
    pdf.bullet("AGMARKNET - Data.gov.in. Agricultural Marketing Information Network.")
    pdf.bullet("NASA POWER - Prediction of Worldwide Energy Resources. https://power.larc.nasa.gov/")
    pdf.bullet("Open-Meteo - Free Weather API. https://open-meteo.com/")
    pdf.bullet("IRRI Rice Knowledge Bank - International Rice Research Institute.")
    pdf.bullet("ICAR - Indian Council of Agricultural Research.")
    pdf.bullet("FAO - Food and Agriculture Organization Plant Health Guidelines.")

    # Save
    out_path = os.path.join(os.path.dirname(__file__), "FarmFriend_Project_Report.pdf")
    pdf.output(out_path)
    print(f"Report saved to: {out_path}")
    return out_path


if __name__ == "__main__":
    build()
