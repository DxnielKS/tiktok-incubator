FROM python:3.9.13-slim

# Set up working directory
WORKDIR /app


# Copy the Python requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


# Copy the rest of the application
COPY . .



# Install dependencies for imagemagick and ffmpeg
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y lsb-release gnupg curl \
    && curl -sL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y nodejs && apt-get install -y git && apt-get install -y imagemagick

# RUN cd TiktokAutoUploader/tiktok_uploader/tiktok-signature && npm i && npx playwright install && npm install playwright-chromium && npx playwright install chromium

# After installing ImageMagick, modify the security policy to prevent the error
RUN sed -i 's/ rights="none" pattern="PDF" / rights="read|write" pattern="PDF" /' /etc/ImageMagick-6/policy.xml \
    && sed -i 's/ rights="none" pattern="EPS" / rights="read|write" pattern="EPS" /' /etc/ImageMagick-6/policy.xml \
    && sed -i 's/ rights="none" pattern="PS" / rights="read|write" pattern="PS" /' /etc/ImageMagick-6/policy.xml

# modify ImageMagick policy file so that Textclips work correctly.
RUN sed -i 's/none/read,write/g' /etc/ImageMagick-6/policy.xml

# The error above is related to ImageMagick's security policies which prevent certain operations.
# To fix this, we need to modify the policy to allow the operation that is failing.
# The specific policy that needs to be changed is the one that restricts the rights to read and write files.
# We will use sed to modify the policy file directly to allow read and write operations for all files.

RUN sed -i 's/rights="none" pattern="@"/rights="read|write" pattern="@"/' /etc/ImageMagick-6/policy.xml

# The error message indicates that ImageMagick's security policy is preventing operations due to size limits.
# To resolve this, we need to adjust the policy to allow larger image sizes.
# We will modify the policy file to remove the size restrictions for images.

RUN sed -i '/disable ghostscript format types/,+6d' /etc/ImageMagick-6/policy.xml \
    && sed -i '/pattern="PDF"/d' /etc/ImageMagick-6/policy.xml \
    && sed -i '/pattern="EPS"/d' /etc/ImageMagick-6/policy.xml \
    && sed -i '/pattern="PS"/d' /etc/ImageMagick-6/policy.xml \
    && sed -i '/pattern="@"/d' /etc/ImageMagick-6/policy.xml
# End Generation Here

# The error message indicates that ImageMagick's security policy is preventing operations due to size limits.
# To resolve this, we need to adjust the policy to allow larger image sizes.
# We will modify the policy file to remove the size restrictions for images.

RUN sed -i '/<policy domain="resource" name="width" value="16KP"/d' /etc/ImageMagick-6/policy.xml \
    && sed -i '/<policy domain="resource" name="height" value="16KP"/d' /etc/ImageMagick-6/policy.xml \
    && sed -i '/<policy domain="resource" name="area" value="128MB"/d' /etc/ImageMagick-6/policy.xml \
    && sed -i '/<policy domain="resource" name="memory" value="256MB"/d' /etc/ImageMagick-6/policy.xml \
    && sed -i '/<policy domain="resource" name="map" value="512MB"/d' /etc/ImageMagick-6/policy.xml \
    && sed -i '/<policy domain="resource" name="disk" value="1GB"/d' /etc/ImageMagick-6/policy.xml
# End Generation Here

RUN echo '<?xml version="1.0" encoding="UTF-8"?>\n\
<!DOCTYPE policymap [\n\
  <!ELEMENT policymap (policy)*>\n\
  <!ATTLIST policymap xmlns CDATA #FIXED ''>\n\
  <!ELEMENT policy EMPTY>\n\
  <!ATTLIST policy xmlns CDATA #FIXED '' domain NMTOKEN #REQUIRED\n\
    name NMTOKEN #IMPLIED pattern CDATA #IMPLIED rights NMTOKEN #IMPLIED\n\
    stealth NMTOKEN #IMPLIED value CDATA #IMPLIED>\n\
]>\n\
<policymap>\n\
  <policy domain="resource" name="memory" value="256MiB"/>\n\
  <policy domain="resource" name="map" value="512MiB"/>\n\
  <policy domain="resource" name="width" value="256KP"/>\n\
  <policy domain="resource" name="height" value="256KP"/>\n\
  <policy domain="resource" name="area" value="128MP"/>\n\
  <policy domain="resource" name="disk" value="1GiB"/>\n\
  <policy domain="path" rights="read|write" pattern="@*"/>\n\
  <policy domain="delegate" rights="none" pattern="URL"/>\n\
  <policy domain="delegate" rights="none" pattern="HTTPS"/>\n\
  <policy domain="delegate" rights="none" pattern="HTTP"/>\n\
  <policy domain="coder" rights="none" pattern="PS"/>\n\
  <policy domain="coder" rights="none" pattern="PS2"/>\n\
  <policy domain="coder" rights="none" pattern="PS3"/>\n\
  <policy domain="coder" rights="none" pattern="EPS"/>\n\
  <policy domain="coder" rights="none" pattern="PDF"/>\n\
  <policy domain="coder" rights="none" pattern="XPS"/>\n\
</policymap>' > /etc/ImageMagick-6/policy.xml

RUN cd TiktokAutoUploader/tiktok_uploader/tiktok-signature && npm i && npx playwright install && npx playwright install-deps


# Run the application
CMD ["python", "-m", "incubator"]