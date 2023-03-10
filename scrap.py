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
from selenium.webdriver.common.action_chains import ActionChains
from db_util import db
import re
from tqdm import tqdm
handler=open("error.txt","w")
db=db("database.db")


x0=1
y0=1
z0=1
t0=1

d_id=0
l_id=0
w_id=0
p_id=0

# Create an instance of ChromeOptions
chrome_options = Options()

# Set Chrome to run in headless mode
chrome_options.add_argument('--headless')

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
driver.get("https://www.sec.kerala.gov.in/public/voters/list")


def scrap() :
    try :
        global x0
        global y0
        global z0
        global t0

        ##################capturing captcha##################

        captcha=driver.find_element(By.XPATH,"/html/body/div[1]/div/section/div/div/div/div[1]/form/div/div[6]/div[2]/div/div[1]/img")
        captch_url = captcha.get_attribute("src")

        # print(captch_url)

        def mousedown(driver,element):
            action_chains = ActionChains(driver)
            action_chains.move_to_element(element)
            action_chains.click_and_hold()
            action_chains.release()
            action_chains.perform()

        def mouseup(driver,element):


            action_chains = ActionChains(driver)
            action_chains.move_to_element(element)
            action_chains.click_and_hold()
            action_chains.release()
            action_chains.perform()

        def getText(element):
            return element.text.split('-')[-1].strip()

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
        captcha_text = pytesseract.image_to_string(img, lang='eng').replace("\n", "")
        # print(captcha_text)

        # img.show()
        # img.save('output.png')

        district_tab=driver.find_element(By.XPATH,"/html/body/div[1]/div/section/div/div/div/div[1]/form/div/div[1]/div/a")
        mousedown(driver, district_tab)
        district_list=driver.find_element(By.XPATH,"/html/body/div[1]/div/section/div/div/div/div[1]/form/div/div[1]/div/div/ul")
        district_list_entry=district_list.find_elements(By.CLASS_NAME,"active-result")

        # print(district_list_entry.get_attribute('innerHTML'))
        # print(district_list_entry)       District element list

        for (x,dist) in enumerate(district_list_entry):
            if x<x0:
                continue
            time.sleep(0.3)

            # print(f'District : {getText(dist)}')
            d_id=db.insert_district(getText(dist))[0][0]
            exec=f"""var element = document.querySelector("li.active-result:nth-child({x+1})"); var event = new MouseEvent('mouseup', {{ bubbles: true, cancelable: true, view: window }}); element.dispatchEvent(event);"""
            driver.execute_script(exec)
            localbody_tab=driver.find_element(By.XPATH,"/html/body/div[1]/div/section/div/div/div/div[1]/form/div/div[2]/div")
            mousedown(driver, localbody_tab)
            time.sleep(0.5)
            localbody_list=driver.find_element(By.XPATH,"/html/body/div[1]/div/section/div/div/div/div[1]/form/div/div[2]/div/div/ul")
            localbody_list_entry=localbody_list.find_elements(By.CLASS_NAME,"active-result")
            # print(localbody_list_entry)

            for (y,ward) in enumerate(localbody_list_entry):
                if y<y0:
                    continue
                time.sleep(0.3)

                l_id=db.insert_localbodie(getText(ward), d_id)[0][0]
                exec=f"""var element = document.querySelector("#lbPublic_chosen > div:nth-child(2) > ul:nth-child(2) > li:nth-child({y+1})"); var event = new MouseEvent('mouseup', {{ bubbles: true, cancelable: true, view: window }}); element.dispatchEvent(event);"""
                driver.execute_script(exec)
                ward_tab=driver.find_element(By.XPATH,'//*[@id="wardPublic_chosen"]')
                mousedown(driver, ward_tab)
                time.sleep(0.5)
                ward_list=driver.find_element(By.XPATH,'/html/body/div[1]/div/section/div/div/div/div[1]/form/div/div[3]/div/div/ul')
                ward_list_entry=ward_list.find_elements(By.CLASS_NAME,"active-result")
                # print(ward_list_entry)

                for (z,polling_station) in enumerate(ward_list_entry):
                    if z<z0:
                        continue
                    time.sleep(0.3)

                    w_id=db.insert_ward(getText(polling_station), l_id)[0][0]
                    exec=f"""var element = document.querySelector('#wardPublic_chosen > div:nth-child(2) > ul:nth-child(2) > li:nth-child({z+1})'); var event = new MouseEvent('mouseup', {{ bubbles: true, cancelable: true, view: window }}); element.dispatchEvent(event);"""
                    driver.execute_script(exec)
                    polling_station_tab=driver.find_element(By.XPATH,'//*[@id="psPublic_chosen"]')
                    mousedown(driver, polling_station_tab)
                    time.sleep(0.5)
                    polling_station_list=driver.find_element(By.XPATH,'/html/body/div[1]/div/section/div/div/div/div[1]/form/div/div[4]/div/div')
                    polling_station_list_entry=polling_station_list.find_elements(By.CLASS_NAME,"active-result")
                    # print(polling_station_list_entry)

                    for (t,lanugage_point) in enumerate(polling_station_list_entry):
                        if t<t0:
                            continue
                        time.sleep(0.3)
                        
                        p_id=db.insert_polling_station(getText(lanugage_point), w_id)[0][0]
                        exec=f"""var element = document.querySelector('#psPublic_chosen > div:nth-child(2) > ul:nth-child(2) > li:nth-child({t+1})'); var event = new MouseEvent('mouseup', {{ bubbles: true, cancelable: true, view: window }}); element.dispatchEvent(event);"""
                        driver.execute_script(exec)
                        polling_station_tab=driver.find_element(By.XPATH,'//*[@id="form_language_chosen"]')
                        mousedown(driver, polling_station_tab)
                        time.sleep(0.1)
                        
                        exec=f"""var element = document.querySelector('#form_language_chosen > div:nth-child(2) > ul:nth-child(2) > li:nth-child(2)'); var event = new MouseEvent('mouseup', {{ bubbles: true, cancelable: true, view: window }}); element.dispatchEvent(event);"""
                        driver.execute_script(exec)

                        driver.execute_script(f"document.querySelector('#form_captcha').setAttribute('value','{captcha_text.strip()}')")
                        driver.find_element(By.XPATH,'//*[@id="form_Search"]').click()


                        def  getTableData(driver):
                            time.sleep(3)
                            table=driver.find_element(By.XPATH,"/html/body/div[1]/div/section/div/div/div/div[2]/div/div/div/div/form")
                            rows=table.find_elements(By.TAG_NAME,'tr')
                            for entry in tqdm(rows,desc=f"[{x0},{y0},{z0},{t0}] >> "):
                                cell=entry.find_elements(By.TAG_NAME,'td')
                                if len(cell) > 1:
                                    try:
                                        cell5=cell[5].text.split(" / ")
                                        gen=cell5[0]
                                        age=cell5[1]
                                    except:
                                        cell5=cell[5].text.split(" / ")
                                        gen=cell5[0]
                                        age=""
                                    # print(f'sl : {cell[0].text}, name : {cell[1].text.replace("DELETED ", "")}, guard : {cell[2].text}, hno : cell[3].text, addr : {cell[4].text}, gen : {gen}, age : {age}, idno : {cell[6].text}, p_id : {p_id}')
                                    try:
                                        db.insert_citizen(cell[1].text.replace("DELETED ", ""), cell[2].text, cell[3].text, cell[4].text, gen, age, cell[6].text, p_id)
                                    
                                    except:
                                        print("error")
                                        print(f'{cell[0].text},{cell[1].text.replace("DELETED ", "")},{cell[2].text},{cell[3].text},{cell[4].text},{gen},{age},{cell[6].text},{p_id}')
                                        handler.write(f'{cell[0].text},{cell[1].text.replace("DELETED ", "")},{cell[2].text},{cell[3].text},{cell[4].text},{gen},{age},{cell[6].text},{p_id}\n')
                                    
                                else:
                                    continue

                                # print(entry)

                        getTableData(driver)
                        # time.sleep(3)
                        # table=driver.find_element(By.XPATH,"/html/body/div[1]/div/section/div/div/div/div[2]/div/div/div/div/form")
                        # print(table)
                        driver.refresh()
                        time.sleep(2)
                        
                        if t0>=(len(polling_station_list_entry) -1 ):
                            t0=1
                            z0=z0+1
                        else:
                            t0=t0+1
                        
                        break
                    
                    if(z0 == (len(ward_list_entry) -1 )):
                        z0=1
                        y0=y=+1
                    break
                
                if y0== (len(localbody_list_entry ) -1) :
                    y0=1
                    x0=x0+1
                break
            if x0 == (len(district_list_entry ) -1) :
                x0=1
            break
        scrap()
        
    except Exception as e:
        print(e)
        scrap()
    
scrap()


input()
handler.close()
db.close()
driver.close()