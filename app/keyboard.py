from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_keyboard = [ KeyboardButton(text='Поиск фильма')],[KeyboardButton(text='Случайный фильм')]

exit_to_main = [[KeyboardButton(text='Вернуться в меню')]]

film_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Добавить в 'Посмотрю позже'", callback_data="watchlist")]
])


main = ReplyKeyboardMarkup(keyboard=main_keyboard, resize_keyboard=True)
exit = ReplyKeyboardMarkup(keyboard=exit_to_main, resize_keyboard=True)

