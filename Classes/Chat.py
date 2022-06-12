from Classes.Message import Message

class Chat():

    def __init__(self, token, owner):
        self.name = f"{owner}'s Chat!"
        self.token = token
        self.members = [owner]
        self.banned_members = []
        self.owner = owner
        self.id = 0
        self.limit = 9
        self.messages = []

    def get_token(self):
        return self.token

    def get_owner(self):
        return self.owner

    def member_join(self, member):
        self.members.append(member)
        return True

    def member_leave(self):
        pass

    def find_member(self, name):
        pass

    def kick_member(self, name, u):
        u.socket.send("| You was kicked from lobby|".encode("utf-8"))
        u.token = 0
        self.members.remove(name)
        return True

    def ban_member(self, name):
        pass

    def unban_member(self, name):
        pass

    def new_message(self, message, author, rmg=True):
        self.messages.append(Message(author, 0, message))
        mg = self.messages[len(self.messages) - 1] # message
        if rmg == True:
            return mg
        else: # rmg = False
            return True

        




