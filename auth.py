import os
import hashlib
import json

USER_DIR = "users"

def get_user_file(username: str) -> str:
    return os.path.join(USER_DIR, f"{username}.json")

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username: str, password: str):
    if not os.path.exists(USER_DIR):
        os.makedirs(USER_DIR)
    
    user_file = get_user_file(username)
    
    if os.path.exists(user_file):
        raise ValueError("User already exists!")
    
    user_data = {
        "username": username,
        "password_hash": hash_password(password)
    }
    
    with open(user_file, "w") as file:
        json.dump(user_data, file)

def authenticate_user(username: str, password: str) -> bool:
    user_file = get_user_file(username)
    
    if os.path.exists(user_file):
        with open(user_file, "r") as file:
            user_data = json.load(file)
            return user_data["password_hash"] == hash_password(password)
    
    return False
