# -*- coding: utf-8 -*-
from dataclasses import dataclass
from configparser import ConfigParser
from environs import Env


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]


@dataclass
class WeatherToken:
    open_weather: str
    yandex: str
    geo_names: str

@dataclass
class Miscellaneous:
    help_msg: str
    parse_mode: str


@dataclass
class Config:
    tg_bot: TgBot
    misc: Miscellaneous


def load_config(env_path: str = None, ini_path: str = None):
    env_reader = Env()
    env_reader.read_env(env_path)

    ini_reader = ConfigParser()
    ini_reader.read(ini_path)

    return Config(
        tg_bot=TgBot(
            token=env_reader.str('BOT_TOKEN'),
            admin_ids=list(map(int, env_reader.list('ADMINS'))),
        ),
        misc=Miscellaneous(
            help_msg=ini_reader.get('MESSAGE', 'help'),
            parse_mode=ini_reader.get('BOT', 'parse_mode'),

        ),
    )
