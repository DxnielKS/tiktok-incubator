FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Install dependencies for imagemagick and ffmpeg
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg imagemagick && \
    rm -rf /var/lib/apt/lists/*

RUN sed -i 's/none/read,write/g' /etc/ImageMagick-6/policy.xml && \
    sed -i '/disable ghostscript format types/,+6d' /etc/ImageMagick-6/policy.xml && \
    sed -i '/policy domain="resource" name="width" value="16KP"/c\  <policy domain="resource" name="width" value="64KP"/' /etc/ImageMagick-6/policy.xml && \
    sed -i '/policy domain="resource" name="height" value="16KP"/c\  <policy domain="resource" name="height" value="64KP"/' /etc/ImageMagick-6/policy.xml

# We need wget to set up the PPA and xvfb to have a virtual screen and unzip to install the Chromedriver
RUN apt-get update && apt-get install -y wget xvfb unzip software-properties-common

# Install Chrome dependencies and fonts
RUN apt-get update && apt-get install -y libx11-6 libxcomposite1 libxcursor1 libxdamage1 libxi6 \
    libxtst6 libnss3 libcups2 libxss1 libxrandr2 libasound2 libpango1.0-0 libatk1.0-0 \
    libatk-bridge2.0-0 libgtk-3-0 libgbm1 fonts-liberation fonts-ipafont-gothic \
    fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst fonts-freefont-ttf \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Install Chrome dependencies
RUN apt-get update && apt-get install -y wget xvfb unzip software-properties-common \
    libu2f-udev xdg-utils

# Download and install Chrome manually
RUN wget -q --continue -O /tmp/google-chrome-stable_current_amd64.deb "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" && \
    dpkg -i /tmp/google-chrome-stable_current_amd64.deb; apt-get -fy install; rm /tmp/google-chrome-stable_current_amd64.deb

RUN find / -name "google-chrome*"

# Set up Chromedriver Environment variables
ENV CHROMEDRIVER_VERSION 2.19
ENV CHROMEDRIVER_DIR /chromedriver
RUN mkdir $CHROMEDRIVER_DIR

# Download and install Chromedriver
RUN wget -q --continue -P $CHROMEDRIVER_DIR "http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip" && \
    unzip $CHROMEDRIVER_DIR/chromedriver* -d $CHROMEDRIVER_DIR

# Put Chromedriver into the PATH
ENV PATH $CHROMEDRIVER_DIR:$PATH

CMD ["python", "-m", "incubator"]