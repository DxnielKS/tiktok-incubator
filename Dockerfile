FROM python:3.9.13-slim

# Set up working directory
WORKDIR /app

# RUN apt-get update && apt-get install -y git \
#     && git clone https://github.com/redrickh/tiktok-uploader \
#     && cd tiktok-uploader && pip install .

# Copy the Python requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


RUN apt-get update && apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_4.x | bash -
RUN apt-get install -y nodejs
# RUN git clone https://github.com/makiisthenes/TiktokAutoUploader
RUN cd TiktokAutoUploader && pip install -r requirements.txt
RUN cd tiktok_uploader/tiktok-signature && npm i && cd ../../..

# Copy the rest of the application
COPY . .

# Run the application
CMD ["python", "-m", "incubator"]