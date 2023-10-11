import numpy as np


GRAVITY = np.array((0., -9.8, 0.), dtype="f4")  # m/s^2


class Particle:
    position = np.zeros(3)
    velocity = np.zeros(3)
    acceleration = np.zeros(3)
    mass = float('inf')

    damping = 0.999
    inverseMass = 0.
    forceAccum = np.zeros(3)

    def integrate(self, duration):
        assert duration > 0

        self.position += self.velocity * duration   # update position
        resultingAcc = self.acceleration            # update acceleration
        resultingAcc += self.forceAccum * duration
        self.velocity += resultingAcc * duration    # update velocity
        self.velocity *= pow(self.damping, duration)


if __name__ == "__main__":
    p = Particle()
    p.position = np.array((0., 0., 0.), dtype="f4")
    p.velocity = np.array((0., 0., 0.), dtype="f4")
    p.acceleration = np.array((0., 0., 0.), dtype="f4")
    p.mass = 1.0
    p.damping = 0.999
    p.inverseMass = 1.0 / p.mass
    p.forceAccum = np.array((0., 0., 0.), dtype="f4")

    p.forceAccum += GRAVITY * p.mass
    p.integrate(1.0)
    print(p.position)
    print(p.velocity)
    print(p.acceleration)
    print(p.mass)
    print(p.damping)
    print(p.inverseMass)
    print(p.forceAccum)