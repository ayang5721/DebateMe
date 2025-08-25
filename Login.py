import os
import json
from classes import User

users_data = {}
if os.path.exists("Users.json") and os.path.getsize("Users.json") > 0:
    with open ("Users.json", "r") as f:
        users_data = json.load(f)

def login(username, password):
    if username in users_data:
        user_info = users_data[username]
        if user_info["password"] == password:
            return User(username, password, rank = user_info["rank"], take_keys = user_info["take_keys"])    
        else:
            print("Incorrect password.")
            return None
    else:
        print("User not found.")
        return None
        
def createUser(username, password):
    if username in users_data:
        print("User already exists.")
        return None
    new_user = User(username, password)
    users_data.update(new_user.toJson())
    with open("Users.json", "w") as f:
        json.dump(users_data, f, indent=4)
    