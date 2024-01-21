FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Install dependencies for imagemagick and ffmpeg
RUN apt-get update && \
    apt-get install -y --no-install-recommends imagemagick ffmpeg && \
    rm -rf /var/lib/apt/lists/*

CMD ["python", "-m", "incubator"]
