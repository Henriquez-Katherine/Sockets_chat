import hashlib

class Hasher():

    @staticmethod
    def hash(x):
        x = str(x).encode("utf-8")
        sha = hashlib.sha1(x).hexdigest()
        return sha
