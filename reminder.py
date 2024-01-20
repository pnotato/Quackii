class reminder():
    def __init__(self, message, time, user):
        self.message = message
        self.time = time
        self.user = user

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message

    def __eq__(self, other):
        return self.message == other.message and self.time == other.time and self.user == other.user

    def __hash__(self):
        return hash((self.message, self.time, self.user))

    def get_message(self):
        return self.message

    def get_time(self):
        return self.time

    def get_user(self):
        return self.user

    def set_message(self, message):
        self.message = message

    def set_time(self, time):
        self.time = time

    def set_user(self,