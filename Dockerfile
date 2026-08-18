FROM python:3.10-slim

WORKDIR /app

# System deps for LightGBM
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps — server-only (no TensorFlow, saves ~400MB)
COPY requirements-server.txt .
RUN pip install --no-cache-dir -r requirements-server.txt

# Copy backend code
COPY api/ ./api/
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY configs/ ./configs/

# Copy ML models (LightGBM + TFLite crop disease detector)
COPY models/crop_risk_advisor/ ./models/crop_risk_advisor/
COPY models/price_intelligence/ ./models/price_intelligence/
COPY models/crop_disease_detector/crop_disease.tflite ./models/crop_disease_detector/crop_disease.tflite
COPY models/crop_disease_detector/metadata.json ./models/crop_disease_detector/metadata.json


# Copy only the data files the API needs at runtime
COPY data/processed/model/mandi_weather_optimized_lite.parquet ./data/processed/model/mandi_weather_optimized_lite.parquet
COPY data/processed/weather/forecast_maharashtra.parquet ./data/processed/weather/forecast_maharashtra.parquet

# Create directory for live price downloads
RUN mkdir -p ./data/raw/mandi/current

# Render injects a dynamic $PORT env var — expose a placeholder and read it at runtime
EXPOSE 10000

# Use shell form (not exec form) so $PORT is expanded from Render's environment
CMD uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-10000}
