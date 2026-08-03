import json
import os

from data_structures.hash_table import HashTable
from data_structures.bst import BST
from data_structures.max_heap import MaxHeap
from users.security import hash_password, verify_password

DEFAULT_DATA_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "users.json"
)


class User:
    def __init__(self, username, password_hash, score=0):
        self.username = username
        self.password_hash = password_hash
        self.score = score

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
    def __init__(self, filepath=DEFAULT_DATA_FILE):
        self.filepath = filepath
        self.table = HashTable()
        self.bst = BST()
        self.heap = MaxHeap()   
        self._load()

    def _load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for d in data:
                    user = User.from_dict(d)
                    self.table.set(user.username, user)
            except (json.JSONDecodeError, OSError):
                pass
        self._rebuild_indexes()

    def _save(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        data = [user.to_dict() for _key, user in self.table.items()]
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _rebuild_indexes(self):
        pairs = [(user.username, user.score) for _key, user in self.table.items()]
        self.bst.build_from(pairs)
        self.heap.rebuild((score, username) for username, score in pairs)

    def username_exists(self, username):
        return self.table.contains(username)

    def register(self, username, password):
        username = username.strip()
        if not username or not password:
            return False, "username and password cant be empty."
        if self.username_exists(username):
            return False, "this username is alraedy exists."
        user = User(username, hash_password(password), score=0)
        self.table.set(username, user)
        self._save()
        self._rebuild_indexes()
        return True, "account created successfully."

    def login(self, username, password):
        username = username.strip()
        user = self.table.get(username)
        if user is None:
            return False, "this account doesnt exist.", None
        if not verify_password(password, user.password_hash):
            return False, "the password is incorrect.", None
        return True, "login successful.", user


    def add_score(self, username, delta_score):
        user = self.table.get(username)
        if user is None:
            return None
        user.score += delta_score
        self._save()
        self._rebuild_indexes()
        return user.score

    def get_score(self, username):
        return self.bst.search(username)

    def top_players(self, k=10):
        return self.heap.top_k(k)