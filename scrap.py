import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.options import Options
import urllib.request
import base64
from PIL import Image
from io import BytesIO
import pytesseract

# Create an instance of ChromeOptions
chrome_options = Options()

# Set Chrome to run in headless mode
chrome_options.add_argument('--headless')

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
driver.get("https://www.sec.kerala.gov.in/public/voters/list")



##################capturing captcha##################

captcha=driver.find_element(By.XPATH,"/html/body/div[1]/div/section/div/div/div/div[1]/form/div/div[6]/div[2]/div/div[1]/img")
captch_url = captcha.get_attribute("src")

# print(captch_url)

js_script = """
var imageElement = document.evaluate("/html/body/div[1]/div/section/div/div/div/div[1]/form/div/div[6]/div[2]/div/div[1]/img", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;

// Create a new canvas element with the same dimensions as the image
var canvas = document.createElement('canvas');
canvas.width = imageElement.width;
canvas.height = imageElement.height;

// Draw the image onto the canvas
var ctx = canvas.getContext('2d');
ctx.drawImage(imageElement, 0, 0, imageElement.width, imageElement.height);

// Get the data URL of the canvas
window.dataURL = canvas.toDataURL();

"""

driver.execute_script(js_script)

img_blob_string = driver.execute_script("return window.dataURL;")
img_blob_string = img_blob_string.split(',')[1]
img_blob_bytes = base64.b64decode(img_blob_string)
img = Image.open(BytesIO(img_blob_bytes))
text = pytesseract.image_to_string(img, lang='eng')
print(text)

# img.show()
# img.save('output.png')

district_tab=driver.find_element(By.XPATH,"/html/body/div[1]/div/section/div/div/div/div[1]/form/div/div[1]/div/a").click()
district_list=driver.find_element(By.XPATH,"/html/body/div[1]/div/section/div/div/div/div[1]/form/div/div[1]/div/div/ul")
district_list_entry=district_list.find_elements(By.CLASS_NAME,"active-result")

# print(district_list_entry.get_attribute('innerHTML'))
print(district_list_entry)

# input()

driver.close()