from src import PyGameEngine as pge
import numpy as np


class Shot(pge.Particle):
    def __init__(self, type):
        super().__init__()
        self.type = type.lower()
        self.setCurrentType()


    def setPistol(self):
        self.setMass(0.01)
        self.setDamping(0.99)
        self.setPosition((0., 1., 0.))
        self.setVelocity((200., 200., 0.))
        self.setAcceleration((0., -1., 0.))

    def setArtillery(self):
        self.setMass(200.0)
        self.setDamping(0.99)
        self.setPosition((0., 1., 0.))
        self.setVelocity((50., 50., 0.))
        self.setAcceleration((0., -20., 0.))

    def setFireball(self):
        self.setMass(1.0)
        self.setDamping(0.99)
        self.setPosition((0., 1., 0.))
        self.setVelocity((50., 50., 0.))
        self.setAcceleration((0., -10., 0.))


    def setCurrentType(self):
        if self.type == "pistol":
            self.setPistol()
        elif self.type == "artillery":
            self.setArtillery()
        elif self.type == "fireball":
            self.setFireball()
        else:
            raise ValueError("Invalid type of shot: {}".format(self.type))
        return Shot

if __name__ == "__main__":
    type = "Pistol"
    shot = Shot(type)
    for _ in range(1000):
        shot.integrate(0.01)
        print(shot.position)
    # print(shot.mass)