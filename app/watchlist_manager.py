import json

class WatchlistItem:
    movie_id: str                    
    title: str                      


class WatchlistManager:
    def __init__(self, file_path="app\watchlist.json"):
        self.file_path = file_path
        
    def _load_data(self):
        with open(self.file_path, 'r') as f:
            return json.load(f)    
    
    def _save_data(self, data):
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)    

    def get_user(self, user_id):
        data = self._load_data()
        return data["users"].get(str(user_id))

    def save_user(self, user_id, user_data):
        data = self._load_data()
        data["users"][str(user_id)] = user_data
        data["metadata"]["total_users"] = len(data["users"])
        self._save_data(data)

m = WatchlistManager()
m.get_user(123)
