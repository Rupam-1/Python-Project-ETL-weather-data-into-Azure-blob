#
#
#
#  Copyright (C) 2020 IHS Markit.
#  All Rights Reserved
#
#
#  NOTICE: All information contained herein is, and remains
#  the property of IHS Markit and its suppliers,
#  if any. The intellectual and technical concepts contained
#  herein are proprietary to IHS Markit and its suppliers
#  and may be covered by U.S. and Foreign Patents, patents in
#  process, and are protected by trade secret or copyright law.
#  Dissemination of this information or reproduction of this material
#  is strictly forbidden unless prior written permission is obtained
#  from IHS Markit.
#
#
#

from helpers.logging_client import LoggerManager
import requests
from requests.auth import HTTPBasicAuth


class WeatherClient:
    def __init__(
        self, api_key, weather_url, lat, lon, units, logger_name, account, crontimeinhhmmss, **kwargs
    ):
        """
        Initializes the DummyAPIClient with user credentials and logging setup.

        Parameters:
            - api_key: The API key for getting the weather data.
            - weather_url: The URL of the weather API.
            - lat: Latitude.
            - lon: Longitude.
            - units: Units of measurement (e.g., metric(for Celcius), imperial(for Farenheit))
            - logger_name: Name of the logger.
            - account: Account information.
            - crontimeinhhmmss: Cron time in hhmmss format.
        """
        
        self.api_key = api_key
        self.weather_url = weather_url
        self.lat = lat
        self.lon = lon
        self.units = units
        self.conn = None
        self.exceptions = []

        self.logger, self.log_location = LoggerManager.getLogger(
            logger_name, account, crontimeinhhmmss, location=True
        )

    def get_data(self, url, params):
        exceptions, json_data = list(), list()
        status = "FAIL"
        try:
            self.logger.info(f"Fetching weather data from the url : {self.weather_url}")
            data = requests.get(url, params=params)
            
            if data.status_code == 200:
                self.logger.info(f"Response status: {data.status_code}")
                self.logger.info("Data fetched successfully...")
                json_data = data.json()
                self.logger.info(f"Length of data : {len(json_data)}")
                status = "SUCCESS"
            else:
                self.logger.error(f"Failed to fetch data. Status code: {data.status_code}")
            
        except Exception as e:
            print(f"Exception happened : {e.args}")
            self.logger.exception(f"Exception happened : {e.args}")
            exceptions.append(str(e))
        
        return json_data, status, ", ".join(exceptions)    
            
    def get_weather_data(self):
        params = {
            'lat': self.lat,
            'lon': self.lon,
            'appid': self.api_key,
            'units': self.units
        }
        return self.get_data(self.weather_url, params)
