from ..env_reader import env_reader
env = env_reader()
DEBUG = env.get("DEBUG")