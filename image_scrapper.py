import io
import os
import time
import base64
import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By

import argparse

# Handle arguments
PROG_DESCRIPTION = """\
description:
  This program scratch images from google search engine.
"""

PROG_EPILOG = """\

"""
label = 'cass'
save_path = os.getcwd()
xpath = 'Q4LuWd'
# Create the argument parser
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=PROG_DESCRIPTION,
    epilog=PROG_EPILOG,)

# Add arguments
parser.add_argument('-l', '--label', dest="label", default=label, type=str, help='label name')
parser.add_argument('-p', '--path', dest="save_path", default=save_path, type=str, help='save path')
parser.add_argument('-x', '--xpath', dest="xpath",default=xpath,  type=str, help='XPath for the XML tag that contains the image link.')

# Parse the arguments
args = parser.parse_args()

if not os.path.exists(args.save_path):
    os.makedirs(args.save_path, exist_ok=True)
    print("Making Directory")
else:
    print("Directory exists")

# List all files in the directory
file_name = []
files = os.listdir(args.save_path)
if files:
    for file in files:
        file_path = os.path.join(args.save_path, file)
        if os.path.isfile(file_path):
            parts = file.split(".")
            file_name.append(int(parts[0]))

    first_file_name = max(file_name) + 1
else:
    first_file_name = 1

print("first file name  :-: ", first_file_name)

options = ChromeOptions()
options.add_argument("--start-maximized")
# options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(options=options)

url = ("https://www.google.com/search?q={s}&tbm=isch&tbs=sur%3Afc&hl=en&ved=0CAIQpwVqFwoTCKCa1c6s4-oCFQAAAAAdAAAAABAC&biw=1251&bih=568")

print("URL :-: ", url)
driver.get(url.format(s=args.label))

for x in range(10):
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    time.sleep(2)

imgResults = driver.find_elements(By.XPATH,f"//img[contains(@class, {xpath})]")
src = [img.get_attribute('src') for img in imgResults]
print("Number of images :-: ", len(src))

for i in range(len(src)):
    # check if the image is None
    if src[i] is None:
        pass
    else:
        # if it's base64 images
        if src[i].startswith('data'):
            imgdata = base64.b64decode(str(src[i]).split(',')[1])
            img = Image.open(io.BytesIO(imgdata))
            img.save(f"{args.save_path}/{first_file_name}.png")
        # if it's image url
        else:
            img = Image.open(requests.get(src[i], stream=True).raw).convert('RGB')
            img.save(f"{args.save_path}/{first_file_name}.jpg")

        first_file_name +=1
    
