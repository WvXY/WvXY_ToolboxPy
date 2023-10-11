from particles import *


class Shot:
    class Pistol:
        


def setCurrentType(type, Shot=Shot()):
    type = type.upper()
    if type == "PISTOL":
        Shot.current = Shot.pistol
    elif type == "ARTILLERY":
        Shot.current = Shot.artillery
    elif type == "FIREBALL":
        Shot.current = Shot.fireball