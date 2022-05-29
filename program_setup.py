import os

def load_program():
    import Program
    d = dir(Program)
    
    #if "test" in d:
        #Program.test()
    if "setup" in d:
        Program.setup()
    if "loop" in d:
        while Program.loop() != 1:
            pass
    if "fin" in d:
        Program.fin()

def init_program():
    if "Program.py" in os.listdir() or "Program" in os.listdir():
        load_program()
    else:
        raise Exception("There is no 'Program.py' or 'Program' module in here, sorry")
        
        
init_program()
