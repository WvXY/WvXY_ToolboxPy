from ballistic import Shot
from src.PyGameEngine import Particle
import numpy as np


GRAVITY = np.array([0.0, -9.8, 0.0], dtype="f4")    # earth gravity
global GRAVITY


class Payload:
    def __init__(self, type, count):
        self.type = type
        self.count = count


class FireworkRule:
    def __init__(self, type, ageRange, velocityRange, damping):
        self.type = type
        self.minAge = ageRange[0]
        self.maxAge = ageRange[1]
        self.minVelocity = velocityRange[0]
        self.maxVelocity = velocityRange[1]
        self.damping = damping

        self.payloadCount = 0
        self.payload = Payload(type, self.payloadCount)

    def create(self, firework: Particle, parent:Particle=None):
        r = np.random.randint(0, 100)
        firework.type = self.type
        firework.age = np.random.randint(self.minAge, self.maxAge)
        if parent:
            firework.setPosition(parent.position)
        vel = parent.velocity
        vel += np.random.randint(self.minVelocity, self.maxVelocity)
        firework.setVelocity(vel)

        firework.setMass(1.0)
        firework.setDamping(self.damping)
        firework.setAcceleration(GRAVITY)
        firework.clearAccumulator()


class Firework(Particle):
    def __init__(self):
        super().__init__()
        self.age = 0.0


    def update(self, duration) -> bool:
        self.integrate(duration)
        self.age -= duration
        return self.age < 0.0


class FireworkDemo:
    def initFireworkRules(self, firework: Particle):
        fireworkRules = FireworkRule(
            "firework",
            (2, 5),
            (10, 20),
            0.9)

        fireworkRules.create(firework)

    def create(self, type, parent: Particle=None):
        firework = Firework()
        self.initFireworkRules(firework)
        return firework




if __name__ == "__main__":
    maxFireworks = 100
    duration = 0.1
    for i in range(maxFireworks):
        firework = Firework()
        while(firework.type > 0 and firework.update(duration)):
            rule = FireworkRule()
            rule = rules + firework.type - 1

            firework.type = 0


        fireworkDemo = FireworkDemo()
        fireworkDemo.initFireworkRules(firework)
        print("firework: ", firework.type, firework.age, firework.velocity, firework.position)

