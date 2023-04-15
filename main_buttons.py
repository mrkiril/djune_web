import os

import logging
import asyncio
import aiomisc

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from dotenv import load_dotenv
from aiogram import html
from aiogram.filters import Text
from aiogram import F
from aiogram.utils.keyboard import ReplyKeyboardBuilder


logger = logging.getLogger(__name__)
# Bot token can be obtained via https://t.me/BotFahter

load_dotenv()

TOKEN = os.environ["TG_TOKEN"]

# Dispatcher is a root router
dp = Dispatcher()

# All handlers should be attached to the Router (or Dispatcher)
router = Router()


@router.message(Command("image"))
async def get_random_image(message: types.Message) -> None:
    """
    generate answer to the button push depends on number  1 3 5 7 vs 2 4 6 8
    :param message:
    :return:
    """

    await message.answer(f"https://source.unsplash.com/random/200x200 lalalala")


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
            [
                types.KeyboardButton(text="З пюрешкою"),
                types.KeyboardButton(text="Без пюрешки")
        ],
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Виберіть спосіб подачі",
        # one_time_keyboard=True / False
    )
    await message.answer("Як подавати котлети?", reply_markup=keyboard)


@router.message(Text("З пюрешкою"))
async def cmd_start1(message: types.Message):
     await message.reply("ЗБС")


@router.message(Text("Без пюрешки"))
async def cmd_start2(message: types.Message):
     await message.reply("Так не смачно")


DATA_DICT = {
    "USD": {
        "EUR": 0.9,
        "KRN": 13.03,
        "ZLT": 13.03,
        "GBP": 13.03,
        "YPI": 13.03,
    },
    "EUR": {
        "USD": 1.1,
        "KRN": 13.03,
        "ZLT": 13.03,
        "GBP": 13.03,
        "YPI": 13.03,
    },
    "KRN": {},
    "ZLT": {},
    "GBP": {},
    "YPI": {}
}


DATA_LIST = [
    {"currency": ("USD", "UAH"), "val": 45.03},
    {"currency": ("USD", "EUR"), "val": 0.9},
    {"currency": ("USD", "GBP"), "val": 0.8},
    {"currency": ("USD", "ZLT"), "val": 5.7},
    {"currency": ("UAH", "YPI"), "val": 12.0},
]


@router.message(Command("reply_builder"))
async def reply_builder(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(
        types.KeyboardButton(text="USD"),
        types.KeyboardButton(text="EUR"),
        types.KeyboardButton(text="KRN"),
        types.KeyboardButton(text="ZLT"),
        types.KeyboardButton(text="GBP"),
        types.KeyboardButton(text="YPI"),
    )
    builder.adjust(3, 2)
    await message.answer(
        "Виберіть число:",
        reply_markup=builder.as_markup(resize_keyboard=False, one_time_keyboard=True),
    )


# @router.message(F.text)
# async def cmd_start2(message: types.Message):
#     if message.text == "11":
#         await message.reply(f"LAlala -> {message.text}")
#         return
#     await message.reply("Loser")


@router.message(Command("select_currency"))
async def reply_currency(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(
        types.KeyboardButton(text="USD"),
        types.KeyboardButton(text="EUR"),
        types.KeyboardButton(text="KRN"),
        types.KeyboardButton(text="ZLT"),
    )
    builder.adjust(3)
    await message.answer(
        "Виберіть валюту:",
        reply_markup=builder.as_markup(resize_keyboard=False, one_time_keyboard=True),
    )


async def second_choice(message: types.Message, currency: str) -> types.Message:
    for data in DATA_LIST:
        curr_1 = data["currency"][0]
        curr_2 = data["currency"][1]
        select_curr_1, select_curr_2 = currency.split("/")

        if (
                (curr_1 == select_curr_1 and curr_2 == select_curr_2)
                or (curr_1 == select_curr_2 and curr_2 == select_curr_1)
        ):
            return await message.answer(f"{currency} -> {data['val']}")
    return


@router.message(F.text)
async def echo_handler(message: types.Message) -> None:
    currency = message.text
    if "/" in currency:
        return await second_choice(message, currency)

    builder = ReplyKeyboardBuilder()
    builder.add(
        types.KeyboardButton(text=f"{currency}/USD"),
        types.KeyboardButton(text=f"{currency}/EUR"),
        types.KeyboardButton(text=f"{currency}/KRN"),
        types.KeyboardButton(text=f"{currency}/ZLT"),
    )
    builder.adjust(3)
    await message.answer(
        "Виберіть валюту:",
        reply_markup=builder.as_markup(resize_keyboard=False, one_time_keyboard=True),
    )


async def main() -> None:
    # ... and all other routers should be attached to Dispatcher
    dp.include_router(router)

    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode="HTML")
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
