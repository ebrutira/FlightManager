# Python resmi imajını kullan
FROM python:3.12-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Sistem bağımlılıklarını yükle
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Gerekli Python paketlerini kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Werkzeug sürüm uyumluluğu için düşür
RUN pip install "werkzeug<3.0"

# dbs_in_use klasörünü ve veritabanlarını kopyala
COPY dbs_in_use/ /app/dbs_in_use/

# Diğer uygulama kodlarını kopyala
COPY app.py /app/
COPY main.py /app/
COPY google_api_test.py /app/
COPY templates/ /app/templates/

# Port ayarı
EXPOSE 5000

# Flask uygulamasının dışarıdan erişilebilir olmasını sağla
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Uygulamayı çalıştır
CMD ["python", "app.py"] 