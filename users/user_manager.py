class User:
    def __init__(self, username, password_hash, score=0):
        pass

    def to_dict(self):
        return {
            "username": self.username,
            "password_hash": self.password_hash,
            "score": self.score,
        }

    @staticmethod
    def from_dict(d):
        return User(d["username"], d["password_hash"], d.get("score", 0))


class UserManager:
    def __init__(self):
           pass

    def _load(self):
        pass

    def _save(self):
        pass

    def _rebuild_indexes(self):
        pass

    def username_exists(self):
        pass

    def register(self):
        pass

    def login(self):
        pass

    def add_score(self, username, delta_score):
        pass

    def get_score(self, username):
        pass

    def top_players(self, k=10):
        pass
        