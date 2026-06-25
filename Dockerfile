FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl wget unzip ca-certificates openssl \
    && rm -rf /var/lib/apt/lists/*

# Xray
ARG XRAY_VERSION=v25.1.30
RUN wget -q https://github.com/XTLS/Xray-core/releases/download/${XRAY_VERSION}/Xray-linux-64.zip -O /tmp/xray.zip && \
    unzip -q /tmp/xray.zip -d /tmp && mv /tmp/xray /usr/local/bin/xray && chmod +x /usr/local/bin/xray && rm -rf /tmp/*

# بقیه مثل قبل...

# ── Python deps ───────────────────────────────────────────────────────────────
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── App code ──────────────────────────────────────────────────────────────────
COPY . .

# ── Dirs ──────────────────────────────────────────────────────────────────────
RUN mkdir -p /data/xray-configs /data/certs

# ── Self-signed cert برای TLS (production باید واقعی باشه) ──────────────────
RUN openssl req -x509 -newkey rsa:2048 -nodes \
    -keyout /data/certs/key.pem \
    -out    /data/certs/cert.pem \
    -days   3650 \
    -subj   "/CN=localhost" 2>/dev/null || true

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "1", \
     "--loop", "uvloop", \
     "--http", "h11"]
