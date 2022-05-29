import os

def load_program():
    import Program
    d = dir(Program)
    
    #if "test" in d:
        #Program.test()
    if "setup" in d:
        Program.setup()
    if "loop" in d:
        Program.loop()
    if "fin" in d:
        Program.fin()

def init_program():
    if "Program.py" in os.listdir():
        load_program()
    else:
        print("There is no 'program.py' in here, sorry")
        
        
init_program()
