# Dockerfile template
DOCKERFILE_CONTENT = """
FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["streamlit","run","pages/1_🧬_Bio_Foundry.py"]
"""
with open("deployment/Dockerfile","w") as f:
    f.write(DOCKERFILE_CONTENT)
