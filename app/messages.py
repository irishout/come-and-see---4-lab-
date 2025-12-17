from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import URLInputFile

import app.keyboard as kb
from app.watchlist_manager import WatchlistManager
import movies_data.api_manager as am

import json

router = Router()
m = WatchlistManager() #менеджер для работы с json

#Состояние бота
class MovieSearch(StatesGroup): 
    current_film = State()
    waiting_for_title = State()

def get_data(data):
    title = data["name"] if data["name"] else data["alternativeName"]
    alt_title = data["alternativeName"] if data["alternativeName"] else "Информация отсутсвует"
    description = data["description"] if data["description"] else "Информация отсутсвует"
    raitingkp = data["rating"]["kp"] if int(data["rating"]["kp"]) > 0 else "Информация отсутсвует"
    raitingIMDb = data["rating"]["imdb"] if int(data["rating"]["imdb"]) > 0 else "Информация отсутсвует"
    raitingfilmCritics = data["rating"]["filmCritics"] if int(data["rating"]["filmCritics"]) > 0 else "Информация отсутсвует"
    year = data["year"]

    return title, alt_title, description, raitingkp, raitingIMDb, raitingfilmCritics, year

def photo_answer(title, alt_title, description, raitingkp, raitingIMDb, raitingfilmCritics, year):
    return (f'🎬Название: {title}\n'
                                '\n'
                                f'Альтернативное название:"{alt_title}"\n'
                                '\n'
                                f'📜Описание: {description}\n'
                                '\n'
                                f'⭐️Рейтинги:\n'
                                f'             Кинопоиск: {raitingkp}\n' 
                                f'             IMDb: {raitingIMDb}\n'
                                f'             filmCritics: {raitingfilmCritics}\n'
                                '\n'
                                f'📆Год: {year}')

#команда старт
@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    
    await message.answer(f"Добро пожаловать. Выберете опцию", reply_markup=kb.main)

    #добавляем юзера в json если его там нет
    if m.get_user(message.from_user.id) == None:
        m.save_user(message.from_user.id, {
            'username': message.from_user.username,
            'watchlist': []
        })


#случайный фильм
@router.message(F.text == 'Случайный фильм')
async def random_movie(message: Message, state: FSMContext) -> None:
    try:
        data = am.find_random()    

        while data['poster']["url"] == None:
            data = am.find_random()
            
        url = data['poster']["url"]
        photo = URLInputFile(url)
   
        title, alt_title, description, raitingkp, raitingIMDb, raitingfilmCritics, year = get_data(data) 
        flag = m.is_film_in_watchlist(message.from_user.id, data["id"])
        await message.answer('Ваш фильм:',reply_markup=kb.main)
        await message.answer_photo(photo,caption= photo_answer(title, alt_title, description, raitingkp, raitingIMDb, raitingfilmCritics, year),
                                    reply_markup= kb.remove_film if flag else kb.film_menu
                                    )
        id_and_title = [data["id"], title]
        await state.update_data(current_film = id_and_title)
        
    except Exception as e:
        await message.answer("Что-то пошло не так", reply_markup=kb.main)
        await print("Ошибка:", e)       
    

#поиск фильма
@router.message(F.text == 'Поиск фильма')
async def movie_search(message: Message, state: FSMContext) -> None:
    await message.answer('Введите название фильма', reply_markup=kb.exit)
    await state.set_state(MovieSearch.waiting_for_title)

#отображение фильма
@router.message(MovieSearch.waiting_for_title)
async def print_movie_by_name(message: Message, state: FSMContext) -> None:
    movie_title = message.text

    if movie_title != "Вернуться в меню":
        try:
            data = am.find_by_name(movie_title)["docs"][0]

            url = data['poster']["url"]
            photo = URLInputFile(url)

            title, alt_title, description, raitingkp, raitingIMDb, raitingfilmCritics, year = get_data(data)

            id_and_title = [data["id"], title]   
            flag = m.is_film_in_watchlist(message.from_user.id, data["id"])
            print(flag)
            await message.answer('Ваш фильм:',reply_markup=kb.exit)
            await message.answer_photo(photo,caption= photo_answer(title, alt_title, description, raitingkp, raitingIMDb, raitingfilmCritics, year),
                                        reply_markup= kb.remove_film if flag else kb.film_menu
                                        ) 
            await state.update_data(current_film = id_and_title)

        except Exception as e:
            await message.answer("Что-то пошло не так. Попробуйте ввести другое название", reply_markup=kb.exit)
            await print("Ошибка:", e)
            
    else:
        await message.answer("Главное меню",reply_markup=kb.main)
        await state.clear()

@router.callback_query(F.data == 'add_to_watchlist')
async def add_to_watchlist(callback: CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id
    id_and_title = await state.get_data()
    id = id_and_title['current_film'][0]
    title = id_and_title['current_film'][1]
    
    if not m.is_film_in_watchlist(user_id, id):
        result = m.save_film(user_id, id, title)
        if result == "Превышен лимит фильмов в watchlist":
            await callback.answer('Превышен лимит фильмов в watchlist')
            return None

        await callback.message.edit_reply_markup(reply_markup=kb.remove_film)
        await callback.answer('Вы добавили фильм')
    else:
        await callback.answer('Фильм уже у вас в watchlist')

@router.callback_query(F.data == 'remove_from_watchlist')
async def remove_from_watchlist(callback: CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id
    id_and_title = await state.get_data()
    id = id_and_title['current_film'][0]
    title = id_and_title['current_film'][1]

    m.delete_film(user_id, id, title)
    await callback.message.edit_reply_markup(reply_markup=kb.film_menu)
    await callback.answer('Вы удалили фильм')

@router.message(F.text == "Мой watchlist")
async def show_watchlist_menu(message: Message):
    user_id = message.from_user.id
    user = m.get_user(user_id)

    if not user or not user.get("watchlist"):
        await message.answer("Ваш список пуст. Добавьте фильмы")
        return None

    watchlist = user["watchlist"] 
    if not watchlist:
        await message.answer("Ваш список пуст. Добавьте фильмы")
        return None
    keyboard = kb.get_watchlist(user_id)
    await message.answer("Ваш список:", reply_markup=keyboard) 

@router.callback_query(F.data.startswith("view_film:"))
async def view_film_from_watchlist(callback: CallbackQuery, state: FSMContext):
    movie_id = callback.data.split(":", 1)[1]  # "view_film:515" → "515"

    #Достаём фильм из watchlist пользователя
    user_id = callback.from_user.id
    user = m.get_user(user_id)
    if not user:
        await callback.answer("Пользователь не найден.", show_alert=True)
        return

    film = next(
        (f for f in user.get("watchlist", []) if str(f["movie_id"]) == movie_id),
        None
    )

    if not film:
        await callback.answer("Фильм не найден.", show_alert=True)
        return

    #Показываем карточку фильма 
    data = am.find_by_id(movie_id)
    url = data['poster']["url"]
    photo = URLInputFile(url)

    title, alt_title, description, raitingkp, raitingIMDb, raitingfilmCritics, year = get_data(data)

    id_and_title = [data["id"], title]   
    flag = m.is_film_in_watchlist(callback.from_user.id, data["id"])
    
    await callback.message.answer('Ваш фильм:',reply_markup=kb.exit)
    await callback.message.answer_photo(photo,caption= photo_answer(title, alt_title, description, raitingkp, raitingIMDb, raitingfilmCritics, year), 
                                        reply_markup= kb.remove_film if flag else kb.film_menu
                                ) 
    await state.update_data(current_film = id_and_title)
    await callback.answer() 


@router.message()
async def unexpected_message(message: Message) -> None:

    await message.answer(f"Неожиданное сообщение. Выберете опцию", reply_markup=kb.main)

