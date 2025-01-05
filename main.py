import openmeteo_requests
import pandas as pd
import requests_cache
import streamlit as st
from retry_requests import retry

from colors import determine_blanket_color

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below

current_date = pd.Timestamp.now().strftime("%Y-%m-%d")
first_day_of_month = pd.Timestamp.now().replace(day=2).strftime("%Y-%m-%d")
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 51.8197,
    "longitude": 19.3038,
    "daily": ["temperature_2m_max", "temperature_2m_min"],
    "timezone": "auto",
    "start_date": first_day_of_month,
    "end_date": current_date,
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]


# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()

daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy().round()


daily_data = {
    "data": pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s", utc=True),
        end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=daily.Interval()),
        inclusive="left",
    ).strftime("%Y-%m-%d"),
}

# daily_data["Maksymalna temperatura"] = f"{daily_temperature_2m_max.round(1)} °C"
daily_data["Maksymalna temperatura °C"] = daily_temperature_2m_max
daily_data["Kolor"] = [
    determine_blanket_color(temperature) for temperature in daily_temperature_2m_max
]

daily_data["image"] = [
    f"app/static/{x.split(' ')[-1]}.jpg" for x in daily_data["Kolor"]
]
st.data_editor(
    daily_data,
    column_config={
        "image": st.column_config.ImageColumn(label="Zdjęcie", width="medium")
    },
    hide_index=True,
)

daily_dataframe = pd.DataFrame(data=daily_data)
# st.write(daily_dataframe)
