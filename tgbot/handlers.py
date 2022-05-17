from aiogram import Router
from aiogram.types import Message
from aiogram.dispatcher.filters.command import CommandStart

basic_router = Router()
weather_router = Router()


@basic_router.message(CommandStart())
async def start_cmd(msg: Message) -> None:
    await msg.reply(f"<b>Привет, {msg.from_user.full_name}!</b>\n\nДля помощи напиши /help")


@basic_router.message(commands=['help'])
async def help_cmd(msg: Message, config) -> None:
    await msg.reply(text=f"{config.misc.help_msg}")

