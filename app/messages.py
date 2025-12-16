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
        #url = data['poster']["url"] if data['poster']["url"] else 'https://media.istockphoto.com/id/1472933890/ru/%D0%B2%D0%B5%D0%BA%D1%82%D0%BE%D1%80%D0%BD%D0%B0%D1%8F/%D0%BD%D0%B5%D1%82-%D0%B2%D0%B5%D0%BA%D1%82%D0%BE%D1%80%D0%BD%D0%BE%D0%B3%D0%BE-%D1%81%D0%B8%D0%BC%D0%B2%D0%BE%D0%BB%D0%B0-%D0%B8%D0%B7%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F-%D0%BE%D1%82%D1%81%D1%83%D1%82%D1%81%D1%82%D0%B2%D1%83%D0%B5%D1%82-%D0%B4%D0%BE%D1%81%D1%82%D1%83%D0%BF%D0%BD%D0%B0%D1%8F-%D0%B8%D0%BA%D0%BE%D0%BD%D0%BA%D0%B0-%D0%BD%D0%B5%D1%82-%D0%B3%D0%B0%D0%BB%D0%B5%D1%80%D0%B5%D0%B8-%D0%B4%D0%BB%D1%8F.jpg?s=612x612&w=0&k=20&c=r3yGvPOiyDFrFiMGfq8K7ObJZwTsMscZug1wqI4Grpo='
        photo = URLInputFile(url)

        title = data["name"] if data["name"] else data["alternativeName"]
        alt_title = data["alternativeName"] if data["alternativeName"] else "Информация отсутсвует"
        description = data["description"] if data["description"] else "Информация отсутсвует"
        raitingkp = data["rating"]["kp"] if int(data["rating"]["kp"]) > 0 else "Информация отсутсвует"
        raitingIMDb = data["rating"]["imdb"] if int(data["rating"]["imdb"]) > 0 else "Информация отсутсвует"
        raitingfilmCritics = data["rating"]["filmCritics"] if int(data["rating"]["filmCritics"]) > 0 else "Информация отсутсвует"
        year = data["year"] 

        await message.answer('Ваш фильм:',reply_markup=kb.exit)
        await message.answer_photo(photo,caption= 
                                f'🎬Название: {title}\n'
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
                                f'📆Год: {year}', reply_markup=kb.main
                                    )
        id_and_title = [data["docs"][0]["id"], title]
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
            data = am.find_by_name(movie_title)  

            url = data["docs"][0]['poster']["url"]
            photo = URLInputFile(url)

            title = data["docs"][0]["name"] if data["docs"][0]["name"] else data["docs"][0]["alternativeName"]
            alt_title = data["docs"][0]["alternativeName"] if data["docs"][0]["alternativeName"] else "Информация отсутсвует"
            description = data["docs"][0]["description"] if data["docs"][0]["description"] else "Информация отсутсвует"
            raitingkp = data["docs"][0]["rating"]["kp"] if int(data["docs"][0]["rating"]["kp"]) > 0 else "Информация отсутсвует"
            raitingIMDb = data["docs"][0]["rating"]["imdb"] if int(data["docs"][0]["rating"]["imdb"]) > 0 else "Информация отсутсвует"
            raitingfilmCritics = data["docs"][0]["rating"]["filmCritics"] if int(data["docs"][0]["rating"]["filmCritics"]) > 0 else "Информация отсутсвует"
            year = data["docs"][0]["year"] 

            id_and_title = [data["docs"][0]["id"], title]   
            flag = m.is_film_in_watchlist(message.from_user.id, data["docs"][0]["id"])
            print(flag)
            await message.answer('Ваш фильм:',reply_markup=kb.exit)
            await message.answer_photo(photo,caption= 
                                    f'🎬Название: {title}\n'
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
                                    f'📆Год: {year}', reply_markup= kb.remove_film if flag else kb.film_menu
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
        m.save_film(user_id, id, title)
        await callback.answer('Вы добавили фильм')
    await callback.answer('Фильм уже у вас в watchlist')

@router.callback_query(F.data == 'remove_from_watchlist')
async def remove_from_watchlist(callback: CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id
    id_and_title = await state.get_data()
    id = id_and_title['current_film'][0]

    m.delete_film_film(user_id, id)

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


@router.message()
async def unexpected_message(message: Message) -> None:

    await message.answer(f"Неожиданное сообщение. Выберете опцию", reply_markup=kb.main)

