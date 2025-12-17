

    Установка
Клонирование репо: https://github.com/irishout/come-and-see---4-lab-.git

    Создание и активация виртуальной среды:

python3 -m venv .venv
source .venv/bin/activate # macOS/Linux
.venv\Scripts\activate # Windows

    Установка зависимостей:

pip install -r requirements.txt

    Добавление апи: 

Создайте файл "api_keys.py" в папке проекта с апи бота BOT_KEY

Создайте файл "kinoAPI.py" в папке movies_data с апи ключем POISKKINO_KEY (https://poiskkino.dev/#)

    Запуск проекта:

python bot.py (или python3 bot.py)
