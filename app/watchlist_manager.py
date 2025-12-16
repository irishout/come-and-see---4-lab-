import json

class WatchlistManager:
    def __init__(self, file_path="app\watchlist.json"):
        self.file_path = file_path
        
    def _load_data(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return json.load(f)    
    
    def _save_data(self, data):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)    

    def get_user(self, user_id):
        data = self._load_data()
        return data["users"].get(str(user_id))

    def save_user(self, user_id, user_data): 
        data = self._load_data()
        data["users"][str(user_id)] = user_data
        data["metadata"]["total_users"] = len(data["users"])
        self._save_data(data)

    def save_film(self, user_id, film_id, film_title): #добавить в watchlist
        data = self._load_data()    
        try:
            if len(data["users"][str(user_id)]['watchlist']) < 10:
                new_film = {
                "movie_id": film_id,
                "movie_title": film_title
                }
                data["users"][str(user_id)]['watchlist'].append(new_film)
                self._save_data(data)
            else:
                return "Превышен лимит фильмов в watchlist"
        except Exception as e:
            return f'Ошибка: {e}'
        
    def delete_film(self, user_id, film_id):
        try:
            film_for_delete = {
                "movie_id": film_id,

                }
            data = self._load_data()
            data["users"][str(user_id)]['watchlist'].remove(film_for_delete)
            self._save_data(data)
        except Exception as e:
            return f'Ошибка: {e}'
    
    def is_film_in_watchlist(self, user_id, film_id):
        try:
            user = self.get_user(user_id)
            if not user:
                return False
            watchlist = user.get("watchlist", [])
            film_id_str = str(film_id)
            return any(str(film.get("movie_id")) == film_id_str for film in watchlist)
        
        except Exception as e:
            return f'Ошибка: {e}'