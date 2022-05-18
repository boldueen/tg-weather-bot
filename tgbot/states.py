# -*- coding: utf-8 -*-
from aiogram.dispatcher.filters.state import StatesGroup, State


class WeatherState(StatesGroup):
    waiting_for_location = State()
