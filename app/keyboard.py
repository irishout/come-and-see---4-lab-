from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard = [[KeyboardButton(text='тестовая конпка'), KeyboardButton(text='Поиск фильма')]]


main = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
