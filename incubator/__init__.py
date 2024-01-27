import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.binary_location = "/var/lib/dpkg/info/google-chrome-stable.postrm"  # Adjust the path to where Chrome is installed
# /var/lib/dpkg/info/google-chrome-stable.postrm
# /var/lib/dpkg/info/google-chrome-stable.list
# /app/google-chrome-stable_current_amd64.deb
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

if not os.path.exists('final-videos'):
    os.mkdir('final-videos')

if not os.path.exists('raw-videos'):
    os.mkdir('raw-videos')

if not os.path.exists("temp-assets"):
    os.mkdir("temp-assets")