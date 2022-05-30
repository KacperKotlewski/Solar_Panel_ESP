from env_reader import Env_reader
env = Env_reader()
DEBUG = False if env.get("DEBUG", 'False') in ['0', 'False'] else True
double_click_time = [int(i) for i in env.get("double_click_time", "(1,0.5)").strip("()").split(",")]
