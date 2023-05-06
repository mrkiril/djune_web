import os

import logging
import asyncio
from typing import Sequence

import aiomisc
import sqlalchemy as sa

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from dotenv import load_dotenv
load_dotenv()
from aiogram import html
from aiogram.filters import Text
from aiogram import F
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from models.base import Currency, db_engine
from models.base import db_session

logger = logging.getLogger(__name__)
# Bot token can be obtained via https://t.me/BotFahter


TOKEN = os.environ["TG_TOKEN"]

# Dispatcher is a root router
dp = Dispatcher()

# All handlers should be attached to the Router (or Dispatcher)
router = Router()


DATA_LIST = [
    {"currency": ("USD", "UAH"), "val": 45.03},
    {"currency": ("USD", "EUR"), "val": 0.9},
    {"currency": ("USD", "GBP"), "val": 0.8},
    {"currency": ("USD", "ZLT"), "val": 5.7},
    {"currency": ("UAH", "YPI"), "val": 12.0},
]


class CurrencyState(StatesGroup):
    first_select = State()
    second_select = State()


def get_keyboard_from_list(currency_name_list: Sequence[str]):
    # currency_name_list = ["USD", "EUR", "ZLT"]
    builder = ReplyKeyboardBuilder()
    keyboard_list = []
    for currency_name in currency_name_list:
        keyboard_list.append(types.KeyboardButton(text=currency_name))

    builder.add(*keyboard_list)
    builder.adjust(3)
    return builder


@router.message(Command("select_currency"))
async def first_select(message: types.Message, state: FSMContext):
    async with db_session.begin() as session:
        resp = await session.scalars(
            sa.select(Currency.currency_from)  # select currency_from from currency;
        )
        currency_from_list: list[str] = resp.all()

    builder = get_keyboard_from_list(currency_name_list=set(currency_from_list))
    await message.answer(
        "Виберіть валюту:",
        reply_markup=builder.as_markup(resize_keyboard=False, one_time_keyboard=True),
    )
    await state.set_state(CurrencyState.first_select)


@router.message(CurrencyState.first_select)
async def second_select(message: types.Message, state: FSMContext) -> None:
    async with db_session.begin() as session:
        resp = await session.scalars(
            sa.select(Currency)
            .where(Currency.currency_from == message.text)  # select * from currency where select_from = 'USD';
        )
        currency_list: list[Currency] = resp.all()

    currency_from_to_list = [
        f"{currency.currency_from}/{currency.currency_to}"
        for currency in currency_list
    ]
    builder = get_keyboard_from_list(currency_name_list=set(currency_from_to_list))
    await message.answer(
        "Виберіть валюту:",
        reply_markup=builder.as_markup(resize_keyboard=False, one_time_keyboard=True),
    )
    await state.set_state(CurrencyState.second_select)


@router.message(CurrencyState.second_select)
async def currency_handler(message: types.Message) -> None:
    currency = message.text  # USD/UAH
    currency_from, currency_to = currency.split("/")
    async with db_session.begin() as session:
        amount = await session.scalar(
            sa.select(Currency.amount)
            .where(
                Currency.currency_from == currency_from,
                Currency.currency_to == currency_to
            )  # select * from currency where currency_from = 'USD' and currency_to = 'EUR';
        )
        return await message.answer(f"{currency} -> {amount}")


@router.message(Command("db"))
async def db_handler(message: types.Message) -> None:
    async with db_session.begin() as session:
        resp = await session.scalars(
            sa.select(Currency)  # select * from currency;
        )
        resp_list: list[Currency] = resp.all()
        print( resp_list )

    await message.answer(f"Виберіть валюту: {len(resp_list)}")


async def main() -> None:

    # ... and all other routers should be attached to Dispatcher
    dp.include_router(router)

    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode="HTML")
    # And the run events dispatching
    await dp.start_polling(bot)
    await db_engine.dispose()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
