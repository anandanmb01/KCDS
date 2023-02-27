import requests
from bs4 import BeautifulSoup


class scrap():

    def __init__(self):
        self.captcha = "cosmic"
        pass

    def fetch(self):
        self.districts = ["KASARGOD", "KANNUR", "WAYANAD", "KOZHIKODE", "MALAPPURAM", "PALAKKAD", "THRISSUR",
                          "ERANAKULAM", "IDUKKI", "KOTTAYAM", "ALAPPUZHA", "PATHANAMTHITTA", "KOLLAM", "TRIRUVANANTHAPURAM"]
        response = requests.get(
            "https://www.sec.kerala.gov.in/public/voters/list")
        self.cookie = response.cookies.get_dict()  # cookie
        # converting to soup
        soup = BeautifulSoup(response.content, "html.parser")
        submit_input = soup.select("#form__token")  # get input form
        self.form_token = submit_input[0].get("value")  # get from data

    def get_local_bodies(self, district_index):
        form_data = {"objid": str(district_index+1)}
        response = requests.post(
            "https://www.sec.kerala.gov.in/public/getalllbcmp/byd", data=form_data, cookies=self.cookie)
        self.local_bodies = response.json()["ops1"]
        return (self.local_bodies)

    def get_wards(self, local_body_index):
        form_data = {"objid": self.local_bodies[local_body_index]['value']}
        response = requests.post(
            "https://www.sec.kerala.gov.in/public/getward/bylb", data=form_data, cookies=self.cookie)
        self.wards = response.json()["ops1"]
        return (self.wards)

    def get_polling_stations(self, ward_index):
        form_data = {"objid": self.wards[ward_index]['value']}
        response = requests.post(
            "https://www.sec.kerala.gov.in/public/getps/byward", data=form_data, cookies=self.cookie)
        self.polling_stations = response.json()["ops1"]
        return (self.polling_stations)

    def get_citizens(self,ward_index,polling_station_index):
        form_data={ "form[ward]": self.wards[ward_index]['value'], "form[pollingStation]": self.polling_stations[polling_station_index]['value'], "form[language]": "E", "form[captcha]": self.captcha, "form[_token]": self.form_token}
        response= requests.post("https://www.sec.kerala.gov.in/public/voters/list",data=form_data,cookies=self.cookie)
        return(response.json()["form"])

    # instance = scrap()
    # instance.fetch()
    # instance.get_local_bodies(0)
    # instance.get_wards(0)
    # instance.get_polling_stations(0)
    # print((instance.get_citizens(0,0)))
