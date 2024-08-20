import os
import json

STORAGE_DIR = "password_storage"

def get_user_storage_file(username: str) -> str:
    return os.path.join(STORAGE_DIR, f"{username}.json")

def save_encrypted_password(username: str, service: str, encrypted_password: str):
    if not os.path.exists(STORAGE_DIR):
        os.makedirs(STORAGE_DIR)
    
    storage_file = get_user_storage_file(username)
    if os.path.exists(storage_file):
        with open(storage_file, "r") as file:
            data = json.load(file)
    else:
        data = {}
    
    data[service] = encrypted_password
    
    with open(storage_file, "w") as file:
        json.dump(data, file)

def retrieve_encrypted_password(username: str, service: str) -> str:
    storage_file = get_user_storage_file(username)
    
    if os.path.exists(storage_file):
        with open(storage_file, "r") as file:
            data = json.load(file)
            return data.get(service)
    return None
