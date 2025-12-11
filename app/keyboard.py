from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = [ KeyboardButton(text='Поиск фильма')], [KeyboardButton(text='Случайный фильм')]
exit_to_main = [[KeyboardButton(text='Вернуться в меню')]]

main = ReplyKeyboardMarkup(keyboard=main_keyboard, resize_keyboard=True)
exit = ReplyKeyboardMarkup(keyboard=exit_to_main, resize_keyboard=True)
