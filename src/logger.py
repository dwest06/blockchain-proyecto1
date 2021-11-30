from datetime import datetime

class Logger():

    def __init__(self, dir:str = None):
        self.dir = dir
        self.logs = []

    def set_dir(self, new_dir:str):
        self.dir = new_dir

    def log(self, message:str):
        log = f"[LOG {datetime.datetime.now()}] - {message}"
        self.logs.append(log)

    def error(self, message:str):
        log = f"[ERROR {datetime.datetime.now()}] - {message}"
        self.logs.append(log)

    def dump_logs(self):
        # Verification dir
        if self.dir is None:
            raise Exception("Dir is None, set directory to dump logs")
        
        logs_file = open(f"logs-{datetime.datetime.now()}.txt", 'w+')

        for log in self.logs:
            logs_file.write(log)

        logs_file.close()
