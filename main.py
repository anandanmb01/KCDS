import concurrent.futures
import multiprocessing
from bs4 import BeautifulSoup
from scrap import *
from db import *
from tqdm import tqdm

db_instance=db("database.db")
db_instance.initilize()
instance = scrap()
instance.fetch()

# Define the list of elements to process
elements=enumerate(instance.districts)
handler.write("DISTRICT,LOCALBODY,WARD,POLLING_STATION,NAME,GUARDIAN,HOUSE_NO,ADDRESS,GENDER,AGE,ID_NO")

    
# Define a function that will process a single element
    
def process_element(element):
    
    (d_id,district)=element
    # db_instance.insert_district(district, d_id)
    
    localbodies=instance.get_local_bodies(d_id)
    for (l_id,x) in enumerate(localbodies):
        
        localbodie=getText(x["text"])
        # db_instance.insert_localbodie(localbodie, d_id)
        wards=instance.get_wards(l_id)
        for (w_id,y) in enumerate(wards):
            ward=getText(y["text"])
            # db_instance.insert_ward(ward, w_id)
            
            polling_stations=instance.get_polling_stations(w_id)
            for (p_id,z) in enumerate(polling_stations):
                polling_station=getText(z["text"])
                # db_instance.insert_polling_station(polling_station, p_id)
                
                # print(f"[{d_id},{l_id},{w_id},{p_id}]")
                citizens_html=instance.get_citizens(w_id, p_id)
                soup = BeautifulSoup(citizens_html, 'html.parser')
                soup = soup.find("form")
                trs = soup.find_all('tr')
                for tr in iter(trs):
                    cell=tr.find_all('td')
                    if len(cell) > 1:
                        try:
                            cell5=cell[5].text.split(" / ")
                            gen=cell5[0]
                            age=cell5[1]
                        except:
                            cell5=cell[5].text.split(" / ")
                            gen=cell5[0]
                            age=""
                        # print(f'sl : {cell[0].text}, name : {cell[1].text.replace("DELETED ", "")}, guard : {cell[2].text}, hno : {cell[3].text}, addr : {cell[4].text}, gen : {gen}, age : {age}, idno : {cell[6].text}, p_id : {p_id}')
                        try:
                            # db.insert_citizen(cell[1].text.replace("DELETED ", ""), cell[2].text, cell[3].text, cell[4].text, gen, age, cell[6].text, p_id)
                            handler.write(f"""{district},{localbodie},{ward},{polling_station},{cell[1].text.replace("DELETED ", "")},{cell[2].text},{cell[3].text},{cell[4].text},{gen},{age},{cell[6].text},\n""")
                        except Exception as e:
                            # handle the error
                            print("An error occurred:", e)
                    else:
                        continue
                    

# Set up a process pool executor with the number of cores
with concurrent.futures.ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
    # Submit a task for each element in the list
    futures = [executor.submit(process_element, element) for element in elements]
    # Wait for all tasks to complete and get the results
    results = [future.result() for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc='Scraping progress')]

print("running sucess")
db_instance.close()
handler.close()
