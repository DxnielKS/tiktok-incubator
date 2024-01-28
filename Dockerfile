FROM python:3.9-slim

# Set up working directory
WORKDIR /app

RUN apt-get update && apt-get install -y git \
    && git clone https://github.com/andrewCohn/tiktok-uploader.git \
    && cd tiktok-uploader && pip install .

RUN apt-get update && apt-get install -y firefox-esr wget \
    && wget -q "https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-linux64.tar.gz" -O /tmp/geckodriver.tar.gz \
    && tar -xzf /tmp/geckodriver.tar.gz -C /usr/local/bin \
    && chmod +x /usr/local/bin/geckodriver \
    && rm /tmp/geckodriver.tar.gz

# Install Chromium
RUN apt-get update && apt-get install -y chromium

# Copy the Python requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Run the application
CMD ["python", "-m", "incubator"]