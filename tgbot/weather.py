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
        '01d': "βοΈ", '01n': "ποΈ",
        '02d': "π€οΈοΈ", '02n': "βπ€οΈ",
        '03d': "π₯οΈοΈ", '03n': "π₯οΈοΈ",
        '04d': "βοΈ", '04n': "βοΈ",
        '09d': "π§οΈοΈ", '09n': "π§οΈοΈ",
        '10d': "βοΈ", '10n': "β",
        '11d': "π©οΈ", '11n': "π©οΈ",
        '13d': "β", '13n': "βοΈ",
        '50d': "πΆβπ«", '50n': "πΆβπ«",
    }

    icon_code = weather_data['current']['weather'][0]['icon']
    rounded_temp = str(round(weather_data['current']['temp'], 1))
    if len(rounded_temp.split('.')) > 1 and rounded_temp.split('.')[1] == '0':
        rounded_temp = rounded_temp.split('.')[0]
    rounded_wind = str(round(weather_data['current']['wind_speed'], 1))
    if len(rounded_wind.split('.')) > 1 and rounded_wind.split('.')[1] == '0':
        rounded_wind = rounded_wind.split('.')[0]
    text += f"<b>{icon[icon_code]}Π‘Π΅Π³ΠΎΠ΄Π½Ρ</b>\n" \
            f"βΠ’Π΅ΠΌΠΏ.: <b><i>{rounded_temp} Β°C</i></b>\n" \
            f"βΠΠ΅ΡΠ΅Ρ: <b><i>{rounded_wind} m/s</i></b>\n\n"

    icon_code = weather_data['daily'][1]['weather'][0]['icon']
    rounded_temp = str(round(weather_data['daily'][1]['temp']['day'], 1))
    if len(rounded_temp.split('.')) > 1 and rounded_temp.split('.')[1] == '0':
        rounded_temp = rounded_temp.split('.')[0]
    rounded_wind = str(round(weather_data['daily'][1]['wind_speed'], 1))
    if len(rounded_wind.split('.')) > 1 and rounded_wind.split('.')[1] == '0':
        rounded_wind = rounded_wind.split('.')[0]
    text += f"<b>{icon[icon_code]}ΠΠ°Π²ΡΡΠ°</b>\n" \
            f"βΠ’Π΅ΠΌΠΏ.: <b><i>{rounded_temp} Β°C</i></b>\n" \
            f"βΠΠ΅ΡΠ΅Ρ: <b><i>{rounded_wind} m/s</i></b>\n\n"

    icon_code = weather_data['daily'][2]['weather'][0]['icon']
    rounded_temp = str(round(weather_data['daily'][2]['temp']['day'], 1))
    if len(rounded_temp.split('.')) > 1 and rounded_temp.split('.')[1] == '0':
        rounded_temp = rounded_temp.split('.')[0]
    rounded_wind = str(round(weather_data['daily'][2]['wind_speed'], 1))
    if len(rounded_wind.split('.')) > 1 and rounded_wind.split('.')[1] == '0':
        rounded_wind = rounded_wind.split('.')[0]
    text += f"<b>{icon[icon_code]}ΠΠΎΡΠ»Π΅Π·Π°Π²ΡΡΠ°</b>\n" \
            f"βΠ’Π΅ΠΌΠΏ.: <b><i>{rounded_temp} Β°C</i></b>\n" \
            f"βΠΠ΅ΡΠ΅Ρ: <b><i>{rounded_wind} m/s</i></b>\n\n"

    icon_code = weather_data['daily'][3]['weather'][0]['icon']
    rounded_temp = str(round(weather_data['daily'][3]['temp']['day'], 1))
    if len(rounded_temp.split('.')) > 1 and rounded_temp.split('.')[1] == '0':
        rounded_temp = rounded_temp.split('.')[0]
    rounded_wind = str(round(weather_data['daily'][3]['wind_speed'], 1))
    if len(rounded_wind.split('.')) > 1 and rounded_wind.split('.')[1] == '0':
        rounded_wind = rounded_wind.split('.')[0]
    text += f"<b>{icon[icon_code]}ΠΠΎΡΠΎΠΌ</b>\n" \
            f"βΠ’Π΅ΠΌΠΏ.: <b><i>{rounded_temp} Β°C</i></b>\n" \
            f"βΠΠ΅ΡΠ΅Ρ: <b><i>{rounded_wind} m/s</i></b>"

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
                        text=f"<b>π ΠΠΎΠ³ΠΎΠ΄Π°</b>\n\n"
                        )
