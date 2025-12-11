from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboard as kb

import movies_data.api_manager as am

router = Router()

#
class MovieSearch(StatesGroup): 
    waiting_for_movie_name = State()

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:

    await message.answer(f"Добро пожаловать. Выберете опцию", reply_markup=kb.main)


@router.message(F.text == 'Поиск фильма')
async def movie_search(message: Message, state: FSMContext) -> None:
    await message.answer('Введите название фильма')
    await state.set_state(MovieSearch.waiting_for_movie_name)

@router.message(MovieSearch.waiting_for_movie_name)
async def printMovie(message: Message, state: FSMContext) -> None:
    movie_title = message.text

    data = am.find_by_name(movie_title)
    await message.answer(data['docs'][0]['name'])



    await state.clear()

