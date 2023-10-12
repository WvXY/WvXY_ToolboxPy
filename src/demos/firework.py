from ballistic import Shot
from src.PyGameEngine import Particle


class FireworkRule:
    def __init__(self, type, ageRange, velocityRange, damping):
        self.type = type
        self.minAge = ageRange[0]
        self.maxAge = ageRange[1]
        self.minVelocity = velocityRange[0]
        self.maxVelocity = velocityRange[1]
        self.damping = damping

        class Payload:
            type = None
            count = 0

        self.payload = Payload()

    def create(self):
        # result = Shot(self.type)
        # result.particle.setMass(1.0)
        # result.particle.setDamping(self.damping)
        # result.particle.setPosition((0., 0., 0.))
        # result.particle.setVelocity((0., self.minVelocity + (self.maxVelocity - self.minVelocity) * random.random(), 0.))
        # result.particle.setAcceleration((0., 0.5, 0.))
        # result.particle.clearAccumulator()
        # result.particle.setMass(1.0)
        # return result
        pass




class Firework(Particle):
    def __init__(self):
        super().__init__()
        self.age = 0.0


    def update(self, duration):
        self.integrate(duration)
        self.age -= duration
        return self.age < 0.0

