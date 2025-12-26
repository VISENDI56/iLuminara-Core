# STAGE 1: The Sovereign Base
FROM python:3.15-rc-alpine3.22 as base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# STAGE 2: The Builder (Compiling Science Kernels)
FROM base as builder
WORKDIR /install
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

# STAGE 3: The Final Sovereign Image
FROM base
WORKDIR /app
COPY --from=builder /install /usr/local
COPY . /app

# SECURITY: Run as non-root user (The "Sentinel" User)
RUN useradd -m sentry && chown -R sentry:sentry /app
USER sentry

# ORCHESTRATION: Launch Overwatch
CMD ["python3", "enterprise/overwatch.py"]