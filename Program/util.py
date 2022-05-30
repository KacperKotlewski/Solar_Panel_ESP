from .settings import DEBUG
def dprint(*args):
    if DEBUG:
        print(*args)