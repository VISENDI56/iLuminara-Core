# FRENASA Symptom Extraction Model - Docker Container
# Designed for deployment on Google Cloud AI Platform (Vertex AI)
# Supports both edge deployment (NVIDIA Jetson) and cloud inference

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy FRENASA engine code
COPY edge_node/frenasa_engine /app/frenasa_engine
COPY edge_node/speech_recognition /app/speech_recognition

# Set Python path
ENV PYTHONPATH=/app

# Expose port for HTTP inference server
EXPOSE 8080

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run the symptom extraction inference server
CMD ["python", "-m", "frenasa_engine.symptom_extractor_server"]
