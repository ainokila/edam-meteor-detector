#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import requests

from datetime import datetime
from source.utils.variables import WEATHER_CONFIG_PATH

class InvalidApiKey(Exception):

    def __init__(self, api_key):
        super().__init__('Invalid API KEY: {}'.format(api_key))


class WeatherDay(object):
    
    def __init__(self, from_dict={}):

        self.moon_phase = int(from_dict.get('moon_phase', 0) * 100)
        self.clouds_percent = from_dict.get('clouds', 0)
        self.description = from_dict.get('weather', [])[0]['description']
        self.icon = from_dict.get('weather', [])[0]['icon']
        self.day_name = datetime.fromtimestamp(from_dict.get('dt', 0)).strftime("%A")


class WeatherAPI(object):

    URL_API = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&appid={}&lang={}&units={}&exclude={}'


    def __init__(self):

        with open(WEATHER_CONFIG_PATH) as weather_file:
            weather_config = json.load(weather_file)

        self.excluded_sections = 'minutely,hourly,alerts'
        self.latitude = weather_config.get('latitude', '0')
        self.longitude = weather_config.get('longitude', '0')
        self.units = weather_config.get('units', 'metric')
        self.lang = weather_config.get('language', 'en')
        self.api_key = weather_config.get('api_key', '')
        self.location = weather_config.get('location', 'Unknown')


    def get_weather_information(self, num_of_days=7):
        """ Returns the weather information for the next N days

        Args:
            num_of_days (int, optional): Number of days to recover weather information. Defaults to 7.

        Raises:
            InvalidApiKey: Invalid API Key used

        Returns:
            list: List with WeatherDay objects
        """
        weather_data = requests.get(self.URL_API.format(self.latitude, self.longitude, self.api_key, self.lang, self.units, self.excluded_sections))

        if weather_data.status_code == 401:
            raise InvalidApiKey(self.api_key)

        weather_days = []
        weather_data_dict = weather_data.json()

        # Fill Current Day
        weather_days.append(WeatherDay(weather_data_dict['current']))

        # Fill Nex N-1 Days
        for day_position in range(0, num_of_days - 1):
            weather_days.append(WeatherDay(weather_data_dict['daily'][day_position]))

        return weather_days

    def get_weather_today(self):
        """ Gets the weather information for today

        Returns:
            WeatherDay: Weather information object
        """
        return self.get_weather_information(num_of_days=1)[0]