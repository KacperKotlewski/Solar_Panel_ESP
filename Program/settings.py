from env_reader import Env_reader
env = Env_reader()
DEBUG = False if env.get("DEBUG", 'False') in ['0', 'False'] else True
time_between_multi_presses, time_from_last_relase = [float(i.strip()) for i in env.get("multi_click_timeing", "(1,0.5)").strip(" ()").split(",")]
