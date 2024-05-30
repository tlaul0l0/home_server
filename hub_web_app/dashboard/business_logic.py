import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import numpy as np

class WeatherAPI:
    def __init__(self):
        self.cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
        self.retry_session = retry(self.cache_session, retries = 5, backoff_factor = 0.2)
        self.openmeteo = openmeteo_requests.Client(session = self.retry_session)

        self.url = "https://api.open-meteo.com/v1/dwd-icon"
        self.params_weather_forecast = {
            "latitude": 47.7333,
            "longitude": 9.25,
            "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_probability_max"],
            "timezone": "Europe/Berlin"
        }
        self.params_weather_hourly = {
            "latitude": 47.7333,
            "longitude": 9.25,
            "hourly": ["temperature_2m"],
            "timezone": "Europe/Berlin",
            "forecast_days": 2
        }

    def get_weather_forecast_data(self):
        """
        returns processed weather forecast data
        @returns: processed weather forecast data
        """
        response = self._make_weather_api_call(param = self.params_weather_forecast)
        processed_data = self._process_weather_forecast_data(raw_data = response)
        return processed_data

    def get_weather_hourly_data(self):
        """
        returns processed weather hourly data
        @returns: processed weather hourly data
        """
        response = self._make_weather_api_call(param = self.params_weather_hourly)
        processed_data = self._process_weather_hourly_data(raw_data = response)
        return processed_data

    def _process_weather_forecast_data(self, raw_data):
        """
        takes raw weather forecast data and processes it
        @param raw_data: data as given from weather api
        @returns: data frame with weather forecast for today + 5 days
        """
        # Process first location. Add a for-loop for multiple locations or weather models
        response = raw_data[0]
        print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
        print(f"Elevation {response.Elevation()} m asl")
        print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
        print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

        # Process daily data. The order of variables needs to be the same as requested.
        daily = response.Daily()
        daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy().round()
        daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy().round()
        daily_precipitation_probability_max = daily.Variables(2).ValuesAsNumpy()

        daily_data = {"date": pd.date_range(
            start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
            end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = daily.Interval()),
            inclusive = "left"
        )}
        daily_data["temperature_2m_max"] = daily_temperature_2m_max
        daily_data["temperature_2m_min"] = daily_temperature_2m_min
        daily_data["precipitation_probability_max"] = daily_precipitation_probability_max

        daily_dataframe = pd.DataFrame(data = daily_data)

        # remove yesterdays data
        daily_dataframe = daily_dataframe.loc[1:]

        return data_frame_to_json(data_frame = daily_dataframe)

    def _process_weather_hourly_data(self, raw_data):
        """
        takes raw weather hourly data and processes it
        @param raw_data: data as given from weather api
        @returns: data frame with hourly weather data of current day
        """
        # Process first location. Add a for-loop for multiple locations or weather models
        response = raw_data[0]
        print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
        print(f"Elevation {response.Elevation()} m asl")
        print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
        print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

        # Process hourly data. The order of variables needs to be the same as requested.
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy().round()

        hourly_data = {"date": pd.date_range(
            start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
            end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = hourly.Interval()),
            inclusive = "left"
        )}
        hourly_data["temperature_2m"] = hourly_temperature_2m

        hourly_dataframe = pd.DataFrame(data = hourly_data)

        today = np.datetime64('today')
        start = f"{today} 00:00:00+00:00"
        end = f"{today+1} 00:00:00+00:00"
        start_index = hourly_dataframe[hourly_dataframe['date'] == start].index.values.astype(int)[0]
        end_index = hourly_dataframe[hourly_dataframe['date'] == end].index.values.astype(int)[0]

        # slice dataframe to leave only weather data for today
        hourly_dataframe = hourly_dataframe.loc[start_index:end_index]

        return data_frame_to_json(data_frame = hourly_dataframe)

    def _make_weather_api_call(self, param):
        """
        executes api call
        @returns: api response
        """
        response = self.openmeteo.weather_api(self.url, params=param)
        return response

def data_frame_to_json(data_frame):
    return data_frame.to_json(indent=4, orient='records', date_format='iso')
