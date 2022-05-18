# -*- coding: utf-8 -*-
import logging

from aiogram import Router, F
from aiogram.dispatcher.filters.command import CommandStart, CommandObject
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, ContentType, ReplyKeyboardRemove

from tgbot.config import Config
from tgbot.states import WeatherState
from tgbot.weather import get_weather

basic_router = Router()
weather_router = Router()


@basic_router.message(CommandStart())
async def start_cmd(msg: Message, state: FSMContext) -> None:
    await state.clear()
    await msg.reply(f"<b>Привет, {msg.from_user.full_name}!</b>\n\nДля помощи напиши /help")


@basic_router.message(commands=['help'])
async def help_cmd(msg: Message, state: FSMContext, config: Config) -> None:
    await state.clear()
    await msg.reply(text=f"{config.misc.help_msg}")


@basic_router.message(commands=["cancel"])
@basic_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """ Cancel any state """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()

    await message.answer(
        "Действие отменено",
        reply_markup=ReplyKeyboardRemove(),
    )


@weather_router.message(commands=['weather'], state="*")
async def weather_cmd(msg: Message, command: CommandObject, state: FSMContext, config: Config) -> None:
    """ Get city name from message or init weather state """
    if not command.args:
        await state.set_state(WeatherState.waiting_for_location)
        await msg.reply("Ожидаю локацию")
    else:
        await msg.reply(await get_weather(config=config, address=command.args))


@weather_router.message(content_types=ContentType.LOCATION, state=WeatherState.waiting_for_location)
async def location_state(msg: Message, state: FSMContext, config: Config) -> None:
    await state.clear()
    await msg.reply(await get_weather(config=config, location=msg.location))
