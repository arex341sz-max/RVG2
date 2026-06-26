FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl wget unzip ca-certificates openssl \
    && rm -rf /var/lib/apt/lists/*

ARG XRAY_VERSION=v25.1.30
RUN wget -q "https://github.com/XTLS/Xray-core/releases/download/${XRAY_VERSION}/Xray-linux-64.zip" -O /tmp/xray.zip \
    && unzip -q /tmp/xray.zip -d /tmp \
    && mv /tmp/xray /usr/local/bin/xray \
    && chmod +x /usr/local/bin/xray \
    && rm -rf /tmp/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ✅ cert داخل /app/certs — داخل image، نه volume /data
RUN mkdir -p /app/certs \
    && openssl req -x509 -newkey rsa:2048 -nodes \
       -keyout /app/certs/key.pem \
       -out    /app/certs/cert.pem \
       -days   3650 \
       -subj   "/CN=rvg-gateway" 2>/dev/null

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
