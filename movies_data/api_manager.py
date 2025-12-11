from movies_data.kinoAPI import POISKKINO_KEY
import requests
import json

# Базовый URL API
base_url = "https://api.poiskkino.dev/v1.4/movie"

headers = {
    "X-API-KEY": POISKKINO_KEY
}


def find_by_name(query:str):
    params = {
        "query": query 
    }

    response = requests.get(base_url + '/search',params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data

    else:
        print(f'Ошибка: {response.status_code}')

def find_random():
    min, max = 6, 10
    # params = {
    #     "status": 'completed', 
    #     "rating.kp": f'{min}-{max}',
    #     "rating.imdb": f'{min}-{max}',
    #     "rating.tmdb": f'{min}-{max}'
    # }

    response = requests.get(base_url + '/random' ,params=None, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data

    else:
        print(f'Ошибка: {response.status_code}')

