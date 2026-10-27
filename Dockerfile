# Runtime image for the Selenium-based Python link checker.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    CHROME_BIN=/usr/bin/chromium \
    TZ=Africa/Kigali

# Install Chromium, its matching WebDriver, and time zone data (log times in Kigali time).
RUN apt-get update \
    && apt-get install -y --no-install-recommends chromium chromium-driver tzdata \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies before copying application code to preserve build cache.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY includes/ ./includes/
RUN mkdir -p /app/logs

CMD ["python", "app.py"]
