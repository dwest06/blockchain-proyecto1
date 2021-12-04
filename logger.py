from datetime import datetime

class Logger():

    def __init__(self, node_id, dir:str = None, show_in_console = True):
        self.node_id = node_id
        self.dir = dir
        self.logs = []
        self.sic = show_in_console

    def set_dir(self, new_dir:str):
        self.dir = new_dir

    def info(self, message:str):
        log = f"[INFO] {self.node_id} {datetime.now()} {message}"
        if self.sic:
            print(log)
        self.logs.append(log)

    def error(self, message:str):
        log = f"[ERROR] {self.node_id} {datetime.now()} {message}"
        if self.sic:
            print(log)
        self.logs.append(log)

    def warning(self, message:str):
        log = f"[WARNING] {self.node_id} {datetime.now()} {message}"
        if self.sic:
            print(log)
        self.logs.append(log)

    def dump_logs(self):
        # Verification dir
        if self.dir is None:
            raise Exception("Dir is None, set directory to dump logs")
        # Write in file
        name = f"{self.node_id}-{datetime.now()}.txt"
        print(f"Writing Logs in {self.dir}/{name}")
        logs_file = open(name, 'w+')
        for log in self.logs:
            logs_file.write(log + '\n')
        logs_file.close()
