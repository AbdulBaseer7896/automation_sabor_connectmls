FROM python:3.9.13

WORKDIR /app

# Copy dependencies first
COPY requirements.txt .

# Upgrade pip + install Python deps
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --default-timeout=100 --retries 10 -r requirements.txt

# Install Chrome & Chromedriver
RUN apt-get update && apt-get install -y wget unzip curl \
    && wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb \
    && CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d '.' -f 1) \
    && CHROMEDRIVER_VERSION=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_$CHROME_VERSION") \
    && wget -q "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip" \
    && unzip chromedriver-linux64.zip \
    && mv chromedriver-linux64/chromedriver /usr/local/bin/ \
    && rm -r chromedriver-linux64.zip chromedriver-linux64 \
    && apt-get clean

# Copy project files
COPY . .

# Run app with Gunicorn
CMD ["gunicorn", "--workers", "4", "--threads", "2", "--bind", "0.0.0.0:5000", "app:app"]
