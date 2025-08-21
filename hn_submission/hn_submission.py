import requests


base_url = "https://api.weather.gov/"

class Client:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_response(self):
        response = requests.get(base_url, verify=False)
        print(f'Status Code:{response.status_code}')
    
    def get_gridpoint_forecast(self, wfo, x, y):
        endpoint = "/gridpoints/{wfo}/{x},{y}"
        gridpoint_url = self.base_url + endpoint
        response = requests.get(gridpoint_url, verify=False)
        if response.status_code == 200:
            print(f'Gridpoint Forecast: {response.json()}')
        
    # def fetch_office_info(self, office_id):
    #     endpoint = "/offices/{office_id}"
    #     office_url = self.base_url + endpoint
    #     response = requests.get(office_url, verify=False)
    #     if response.status_code == 200:
    #         print(f'Office Info: {response.json()}')
    #     else:
    #         print(f"Error fetching office info: {response.status_code}")
    #         return None
       

call_api = Client(base_url)        
call_api.get_response()
call_api.get_gridpoint_forecast("AKQ", 200, 172)
# call_api.fetch_office_info("ALY")
    
    
    

