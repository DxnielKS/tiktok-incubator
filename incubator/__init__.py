import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

if not os.path.exists('final-videos'):
    os.mkdir('final-videos')

if not os.path.exists('raw-videos'):
    os.mkdir('raw-videos')

if not os.path.exists("temp-assets"):
    os.mkdir("temp-assets")