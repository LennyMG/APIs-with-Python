import requests
import json
 
INFILE = './local/input_queries.jsonl'
OUTFILE = './local/output.jsonl'

def retrieveJsonl():
    data = []
    try:
        with open(INFILE, 'r', encoding='utf-8') as file:
            for line in file:
                json_obj = json.loads(line.strip())
                data.append(json_obj)      
            return data
    except FileNotFoundError:
        print("Error: json file not found.")

class Office:
    def __init__(self, office_data):
        self.office_data = office_data
      
    @property
    def office_name(self):
        return self.office_data.get('name', '')
    
    @property
    def office_email(self):
        return self.office_data.get('email', '')
        
class Forecast:
    def __init__(self, forecast_data):
        self.forecast_data = forecast_data
      
    @property
    def periods(self):
        return self.forecast_data.get('properties', {}).get('periods', [])   
    
    @property
    def elevation(self):
        return self.forecast_data.get('properties', {}).get('elevation', {}).get('value', []) 
    
    @property
    def min_temperature(self):
        temperatures = [period.get('temperature') for period in self.periods if 'temperature' in period]
        return round(min(temperatures)) if temperatures else None
    
    @property
    def max_temperature(self):
        temperatures = [period.get('temperature') for period in self.periods if 'temperature' in period]
        return  round(max(temperatures)) if temperatures else None
    
    @property
    def avg_temperature(self):
        temperatures = [period.get('temperature') for period in self.periods if 'temperature' in period]
        return round(sum(temperatures) / len(temperatures)) if temperatures else None
    
    @property
    def avg_probability_precip(self):
        probabilities = []
        for period in self.periods:
            prob = period.get('probabilityOfPrecipitation', {}).get('value')
            if prob is not None:
                probabilities.append(prob)
        return round(sum(probabilities) / len(probabilities)) if probabilities else None
    
    @property
    def max_wind_speed(self):
        wind_speeds = []
        for period in self.periods:
            wind_speed_str = period.get('windSpeed', '')
            if wind_speed_str:
                speeds = [int(s) for s in wind_speed_str.split() if s.isdigit()]
                if speeds:
                    wind_speeds.append(max(speeds))
        return round(max(wind_speeds)) if wind_speeds else None
    
    @property
    def elevation_m(self):
        return round(self.elevation)
        
 
    
    @property
    def elevation_ft(self):
        return round(self.elevation * 3.28084)
    
    
        
class ApiClient:
    def __init__(self, base_url="https://api.weather.gov/"):
        self.base_url = base_url

    def get_forecast(self, office_id, x_coordinate, y_coordinate):
        """
        Fetch forecast data from the /gridpoints/{weather_office}/{x_coordinate},{y_coordinate}/forecast endpoint.
        """
        endpoint = f"/gridpoints/{office_id}/{x_coordinate},{y_coordinate}/forecast"
        forecast_url = self.base_url + endpoint
        response = requests.get(forecast_url, verify=False)
        # print(response.json())
        return response.json()
    
    def get_office(self, weather_office):
        """
        Fetch office information from the /offices/{weather_office} endpoint.
        """
        endpoint = f"/offices/{weather_office}"
        url = self.base_url + endpoint
        response = requests.get(url, verify=False)
        # print(response.json())
        return response.json()

def main():
    data = retrieveJsonl()
    
    with open(OUTFILE, 'w', encoding='utf-8') as outfile:
        for idx, entry in enumerate(data):
                 
            apiObj = ApiClient()
            # apiObj.get_forecast(test['weather_office'], test['x_coordinate'], test['y_coordinate'])
            
            #forecast  raw info and office raw info
            raw_info = apiObj.get_office(entry['weather_office'])
            raw_forecast = apiObj.get_forecast(entry['weather_office'], entry['x_coordinate'], entry['y_coordinate'])
            
            # create Forecast and Office objects
            forecast_obj = Forecast(raw_forecast)
            office_obj=  Office(raw_info)
        
            # Generate output dictionary
            output = {
                "office_name": office_obj.office_name, 
                "office_email":office_obj.office_email, 
                "elevation_ft": forecast_obj.elevation_ft, 
                "elevation_m": forecast_obj.elevation_m, 
                "max_temp_f": forecast_obj.max_temperature, 
                "min_temp_f": forecast_obj.min_temperature, 
                "avg_temp_f": forecast_obj.avg_temperature, 
                "avg_temp_c": forecast_obj.avg_temperature, 
                "avg_probability_precip": forecast_obj.avg_probability_precip,
                "max_wind_speed_mph": forecast_obj.max_wind_speed

            }
                        
            outfile.write(json.dumps(output) + '\n')
    
    
if __name__ == "__main__":
    main()
