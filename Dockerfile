FROM python:3.9-slim

# Set up working directory
WORKDIR /app

# Install Python and Chrome dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    gnupg2 \
    ca-certificates \
    apt-utils \
    software-properties-common \
    unzip \
    xvfb \
    libxi6 \
    libglib2.0-0 \
    libnss3 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxrandr2 \
    libxss1 \
    libxtst6 \
    libcups2 \
    libx11-6 \
    libx11-xcb1 \
    libdbus-1-3 \
    libgtk-3-0 \
    ffmpeg \
    imagemagick \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatspi2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    xdg-utils \
    libgbm1 \
    && rm -rf /var/lib/apt/lists/*

# Copy the Python requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Run the application
CMD ["python", "-m", "incubator"]