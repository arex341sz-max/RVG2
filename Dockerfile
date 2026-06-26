FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl wget unzip ca-certificates openssl \
    && rm -rf /var/lib/apt/lists/*

ARG XRAY_VERSION=v25.1.30
RUN wget -q "https://github.com/XTLS/Xray-core/releases/download/${XRAY_VERSION}/Xray-linux-64.zip" -O /tmp/xray.zip \
    && unzip -q /tmp/xray.zip -d /tmp/xray-extracted \
    && mv /tmp/xray-extracted/xray /usr/local/bin/xray \
    && chmod +x /usr/local/bin/xray \
    && rm -rf /tmp/xray.zip /tmp/xray-extracted

# ✅ geoip و geosite از ریپوی مخصوص v2fly (همیشه آپدیت و stable)
RUN mkdir -p /usr/local/share/xray \
    && wget -q "https://github.com/v2fly/geoip/releases/latest/download/geoip.dat" \
            -O /usr/local/share/xray/geoip.dat \
    && wget -q "https://github.com/v2fly/domain-list-community/releases/latest/download/dlc.dat" \
            -O /usr/local/share/xray/geosite.dat

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ✅ cert داخل /data/certs — همان مسیری که config.py تعریف کرده
RUN mkdir -p /data/certs \
    && openssl req -x509 -newkey rsa:2048 -nodes \
       -keyout /data/certs/key.pem \
       -out    /data/certs/cert.pem \
       -days   3650 \
       -subj   "/CN=rvg-gateway" 2>/dev/null

EXPOSE 8080

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]
