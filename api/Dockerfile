FROM python:3.12-slim

# Security: Run as non-root
RUN groupadd -r iluminara && useradd -r -g iluminara iluminara

WORKDIR /app
COPY requirements-ml.txt .
RUN pip install --no-cache-dir -r requirements-ml.txt

COPY . .
RUN chown -R iluminara:iluminara /app
USER iluminara

EXPOSE 8000
CMD ["uvicorn", "api.server:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]