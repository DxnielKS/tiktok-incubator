FROM python:3.9.13-slim

# Set up working directory
WORKDIR /app


# Copy the Python requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt



# Copy the rest of the application
COPY . .

RUN apt-get update && apt-get install -y lsb-release gnupg curl \
    && curl -sL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y nodejs && apt-get install -y git && apt-get install -y imagemagick

RUN cd TiktokAutoUploader/tiktok_uploader/tiktok-signature && npm i

# Run the application
CMD ["python", "-m", "incubator"]