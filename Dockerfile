FROM python:3.13-slim

# ── System deps ───────────────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl wget unzip ca-certificates openssl \
    && rm -rf /var/lib/apt/lists/*

# ── Xray binary ───────────────────────────────────────────────────────────────
ARG XRAY_VERSION=v25.1.30
ARG TARGETARCH=64

RUN set -e \
    && XRAY_ZIP="Xray-linux-${TARGETARCH}.zip" \
    && wget -q "https://github.com/XTLS/Xray-core/releases/download/${XRAY_VERSION}/${XRAY_ZIP}" -O /tmp/xray.zip \
    && unzip -q /tmp/xray.zip -d /tmp/xray \
    && mv /tmp/xray/xray /usr/local/bin/xray \
    && chmod +x /usr/local/bin/xray \
    && rm -rf /tmp/xray /tmp/xray.zip \
    && xray version

# ── Python deps ───────────────────────────────────────────────────────────────
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── App code ──────────────────────────────────────────────────────────────────
COPY . .

# ── Dirs ──────────────────────────────────────────────────────────────────────
RUN mkdir -p /data/xray-configs /data/certs

# ── Self-signed cert برای TLS ──────────────────────────────────────────────────
RUN openssl req -x509 -newkey rsa:2048 -nodes \
    -keyout /data/certs/key.pem \
    -out    /data/certs/cert.pem \
    -days   3650 \
    -subj   "/CN=localhost"

EXPOSE 8000

# ✅ اصلاح مهم: استفاده از فرمت Shell برای پردازش $PORT
CMD python -m uvicorn main:app \
     --host 0.0.0.0 \
     --port $PORT \
     --workers 1 \
     --loop uvloop \
     --http h11
