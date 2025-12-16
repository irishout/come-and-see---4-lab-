from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import json 



def get_watchlist(user_id):
    with open("app\watchlist.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
        watchlist_keyboard = InlineKeyboardMarkup(inline_keyboard=
        [[InlineKeyboardButton(text=film["movie_title"], callback_data=f'view_film:{str(film["movie_id"])}')] for film in data["users"][str(user_id)]["watchlist"]])
        return watchlist_keyboard


main_keyboard = [[ KeyboardButton(text='Поиск фильма')],[KeyboardButton(text='Случайный фильм')], [KeyboardButton(text='Мой watchlist')]]

exit_to_main = [[KeyboardButton(text='Вернуться в меню')]]

film_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Добавить в 'Посмотрю позже'", callback_data="add_to_watchlist")]
])
remove_film = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Удалить из 'Посмотрю позже'", callback_data="remove_from_watchlist")]
])



main = ReplyKeyboardMarkup(keyboard=main_keyboard, resize_keyboard=True)
exit = ReplyKeyboardMarkup(keyboard=exit_to_main, resize_keyboard=True)

