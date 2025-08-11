


class User:
    def __init__(self, username, password, rank = 0, take_keys = []):
        self.username = username
        self.password = password
        self.rank = rank
        self.take_keys = take_keys

    def toJson(self):
        return {
            self.username: {
            "username": self.username,
            "password": self.password,
            "rank": self.rank,
            "take_keys": self.take_keys
            }
        }
        
    

class Take:

    def __init__(self, key, description, user1, user2, winner, loser):
        self.key = str(key)
        self.description = description
        self.user1 = user1
        self.user2 = user2
        self.winner = winner
        self.loser = loser

    def toJson(self):
        return {
                "key": self.key,
                "description": self.description,
                "user1": self.user1,
                "user2": self.user2,
                "winner": self.winner,
                "loser": self.loser
            
        }