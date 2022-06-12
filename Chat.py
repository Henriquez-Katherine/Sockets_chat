
class Chat():

    def __init__(self, token, owner):
        self.name = "NONE"
        self.token = token
        self.members = [owner]
        self.banned_members = []
        self.owner = owner
        self.id = 0
        self.limit = 9
        self.messages = []

    def get_token(self):
        return self.token

    def find_member(self, name):
    	pass

    def kick_member(self, name):
    	pass

    def ban_member(self, name):
    	pass

    def unban_member(self, name):
    	pass

    def new_message(self, message):
    	pass




