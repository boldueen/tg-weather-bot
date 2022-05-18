# -*- coding: utf-8 -*-
import requests
from aiogram.types import Location

from tgbot.config import Config


def fetch_open_weather(lat: float, lng: float, token: str):
    """ Get weather by cord
        :param lat: float
        :param lng: float
        :param token: str Open weather app id
    """
    params = {
        'lat': lat,
        'lon': lng,
        'appid': token,
        'exclude': 'hourly,minutely',
        'units': 'metric',
        'lang': 'ru'
    }
    response = requests.get('https://api.openweathermap.org/data/2.5/onecall', params=params)
    response = response.json()
    return response


def get_geocode_yandex(place: str, token: str):
    """ Get cords by place name
        :param place: str Place name
        :param token: str Yandex API token
    """
    params = {
        'apikey': token,
        'format': 'json',
        'geocode': place
    }
    response = requests.get('https://geocode-maps.yandex.ru/1.x', params=params)
    response = response.json()
    pos = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
    geocode = {
        'lat': float(pos.split(' ')[1]),
        'lng': float(pos.split(' ')[0])
    }
    return geocode


def text_weather(text: str, weather_data: dict):
    icon = {
        '01d': "☀️", '01n': "🌑️",
        '02d': "🌤️️", '02n': "☀🌤️",
        '03d': "🌥️️", '03n': "🌥️️",
        '04d': "☁️", '04n': "☁️",
        '09d': "🌧️️", '09n': "🌧️️",
        '10d': "☂️", '10n': "☂",
        '11d': "🌩️", '11n': "🌩️",
        '13d': "❄", '13n': "☃️",
        '50d': "😶‍🌫", '50n': "😶‍🌫",
    }

    icon_code = weather_data['current']['weather'][0]['icon']
    rounded_temp = str(round(weather_data['current']['temp'], 1))
    if len(rounded_temp.split('.')) > 1 and rounded_temp.split('.')[1] == '0':
        rounded_temp = rounded_temp.split('.')[0]
    rounded_wind = str(round(weather_data['current']['wind_speed'], 1))
    if len(rounded_wind.split('.')) > 1 and rounded_wind.split('.')[1] == '0':
        rounded_wind = rounded_wind.split('.')[0]
    text += f"<b>{icon[icon_code]}Сегодня</b>\n" \
            f"├Темп.: <b><i>{rounded_temp} °C</i></b>\n" \
            f"└Ветер: <b><i>{rounded_wind} m/s</i></b>\n\n"

    icon_code = weather_data['daily'][1]['weather'][0]['icon']
    rounded_temp = str(round(weather_data['daily'][1]['temp']['day'], 1))
    if len(rounded_temp.split('.')) > 1 and rounded_temp.split('.')[1] == '0':
        rounded_temp = rounded_temp.split('.')[0]
    rounded_wind = str(round(weather_data['daily'][1]['wind_speed'], 1))
    if len(rounded_wind.split('.')) > 1 and rounded_wind.split('.')[1] == '0':
        rounded_wind = rounded_wind.split('.')[0]
    text += f"<b>{icon[icon_code]}Завтра</b>\n" \
            f"├Темп.: <b><i>{rounded_temp} °C</i></b>\n" \
            f"└Ветер: <b><i>{rounded_wind} m/s</i></b>\n\n"

    icon_code = weather_data['daily'][2]['weather'][0]['icon']
    rounded_temp = str(round(weather_data['daily'][2]['temp']['day'], 1))
    if len(rounded_temp.split('.')) > 1 and rounded_temp.split('.')[1] == '0':
        rounded_temp = rounded_temp.split('.')[0]
    rounded_wind = str(round(weather_data['daily'][2]['wind_speed'], 1))
    if len(rounded_wind.split('.')) > 1 and rounded_wind.split('.')[1] == '0':
        rounded_wind = rounded_wind.split('.')[0]
    text += f"<b>{icon[icon_code]}Послезавтра</b>\n" \
            f"├Темп.: <b><i>{rounded_temp} °C</i></b>\n" \
            f"└Ветер: <b><i>{rounded_wind} m/s</i></b>\n\n"

    icon_code = weather_data['daily'][3]['weather'][0]['icon']
    rounded_temp = str(round(weather_data['daily'][3]['temp']['day'], 1))
    if len(rounded_temp.split('.')) > 1 and rounded_temp.split('.')[1] == '0':
        rounded_temp = rounded_temp.split('.')[0]
    rounded_wind = str(round(weather_data['daily'][3]['wind_speed'], 1))
    if len(rounded_wind.split('.')) > 1 and rounded_wind.split('.')[1] == '0':
        rounded_wind = rounded_wind.split('.')[0]
    text += f"<b>{icon[icon_code]}Потом</b>\n" \
            f"├Темп.: <b><i>{rounded_temp} °C</i></b>\n" \
            f"└Ветер: <b><i>{rounded_wind} m/s</i></b>"

    return text


async def get_weather(config: Config,
                      inline_mode: bool = False,
                      address: str = None,
                      location: Location = None):
    if address:
        geocode = get_geocode_yandex(address, config.weather.yandex)
    elif location:
        geocode = {
            'lat': location.latitude,
            'lng': location.longitude
        }
    else:
        geocode = {
            'lat': '56.1366',
            'lng': '40.3966'
        }

    weather_data = fetch_open_weather(geocode['lat'], geocode['lng'],
                                      config.weather.open_weather)

    return text_weather(weather_data=weather_data,
                        text=f"<b>📍 Погода</b>\n\n"
                        )
