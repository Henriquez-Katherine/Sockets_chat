
class User():

    def __init__(self, name, rank, status):
        self.name = name
        self.token = 0
        self.rank = rank
        self.status = status

    def get_name(self):
    	return self.name

    def get_rank(self):
    	return self.rank

    def get_status(self):
    	return self.status


