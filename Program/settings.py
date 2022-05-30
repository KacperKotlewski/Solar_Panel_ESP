from env_reader import Env_reader
env = Env_reader()
DEBUG = False if env.get("DEBUG") in ['0', 'False'] else True
