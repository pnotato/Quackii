from pymongo import MongoClient

class Database:

    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.duckydb
        self.messages = self.db.messages

    def insert_message(self, user, message):
        self.messages.insert_one({"user": user, "message": message})

    def get_messages(self):
        messagelist = []
        for user in self.messages.find():
            messagelist.append(user)
        return messagelist

    # clears all messages
    def delete_messages(self):
        self.messages.delete_many({})

# usage
#database = Database()
#database.insert_message("Ducky", "Hello, world!")
#database.insert_message("Ducky", "How are you?")
#database.insert_message("Ducky", "Goodbye!")
#print(database.get_messages())
#database.delete_messages()
