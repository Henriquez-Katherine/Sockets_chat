class Logger():
    
    @staticmethod
    def create_log_file():
        log = open('log.txt', 'w')
        log.write("#######################")

    @staticmethod
    def log_started():
        log = open('log.txt', 'a')
        log.write("[INFO] SERVER WAS STARTED.")

