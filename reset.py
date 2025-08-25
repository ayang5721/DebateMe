import os
import json

print("This will reset all user data. Are you sure? (yes/no)")
if input().strip().lower() == "yes":
    if os.path.exists("Users.json"):
        with open ("Users.json", "w") as f:
            f.write("")
        print("All user data has been reset.")

print ("This will reset all Takes. Are you sure? (yes/no)")
if input().strip().lower() == "yes":
    with open ("Takes.json", "r") as f:
        takes_data = json.load(f)

    for take in takes_data.values():
        debate_path = f"{take['key']}_debate.jsonl"
        if os.path.exists(debate_path):
            os.remove(debate_path)
    
    if os.path.exists("Takes.json"):
        with open("Takes.json", "w") as f:
            f.write("")

        print("All takes have been reset.")

    if os.path.exists("Users.json") and os.path.getsize("Users.json") > 0 and os.path.getsize("Takes.json") == 0:
        users_data = json.load(open("Users.json", "r"))
        for user in users_data.keys():
            users_data[user]["take_keys"] = []
        with open("Users.json", "w") as f:
            json.dump(users_data, f, indent=4)