from .settings import DEBUG
def dprint(*args):
    if bool(DEBUG):
        print(*args)