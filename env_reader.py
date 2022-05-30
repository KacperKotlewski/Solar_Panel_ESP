import os

class Env_reader:
    def __init__(self, file_to_open=".env"):
        self.file_to_open = file_to_open
        self.env_dict = {}
        self.load_env()
        
    def load_env(self):
        file = self.file_to_open
        if file in os.listdir():
            with open(file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line != "#":
                        line = line.split("=")
                        if len(line) == 2:
                            self.env_dict[line[0].upper()] = line[1]
                        if len(line) > 2:
                            self.env_dict[line[0].upper().strip()] = str.join("=", line[1:]).strip()
        else:
            raise 
                        
    def get(self, key, default=None):
        if key.upper() in self.get_keys():
            return self.env_dict[key.upper()]
        elif default is not None:
            return default
        else:
            raise ValueError("there is no " + key + " in env")
    
    def set(self, key, value):
        self.env_dict[key.upper()] = value
        
    def save_env(self):
        file = self.file_to_open
        with open(file, "w") as f:
            for key in self.env_dict:
                f.write(key + "=" + self.env_dict[key] + "\n")
                
    def get_keys(self):
        return self.env_dict.keys()
    
