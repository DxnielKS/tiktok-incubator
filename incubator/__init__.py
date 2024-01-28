import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# options = webdriver.ChromeOptions()
# # Set any options you need
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')

# Now pass the options using the 'options' keyword instead of 'chrome_options'
# driver = webdriver.Chrome(options=options)

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", DesiredCapabilities.CHROME)

if not os.path.exists('final-videos'):
    os.mkdir('final-videos')

if not os.path.exists('raw-videos'):
    os.mkdir('raw-videos')

if not os.path.exists("temp-assets"):
    os.mkdir("temp-assets")