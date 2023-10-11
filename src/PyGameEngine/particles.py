import numpy as np


GRAVITY = np.array((0., -9.8, 0.), dtype="f4")  # m/s^2


class Particle(object):
    def __init__(self):
        self.position = np.zeros(3)
        self.velocity = np.zeros(3)
        self.acceleration = np.zeros(3)
        self.mass = float('inf')
        self.damping = 0.999
        
        self.__inverseMass = 0.
        self.forceAccum = np.zeros(3)
    
    # set methods
    def setVelocity(self, velocity):
        self.velocity = np.array(velocity, dtype="f4")
        
    def setPosition(self, position):
        self.position = np.array(position, dtype="f4")
        
    def setAcceleration(self, acceleration):
        self.acceleration = np.array(acceleration, dtype="f4")
        
    def setMass(self, mass):
        self.mass = float(mass)
        self.__inverseMass = 1.0 / mass
    
    def setDamping(self, damping):
        self.damping = damping
    
    # =================================================================
    # integrate method
    def integrate(self, duration: float) -> None:
        assert duration > 0.

        self.position += self.velocity * duration   # update position
        self.resultingAcc = self.acceleration            # update acceleration
        self.resultingAcc += self.forceAccum * self.__inverseMass
        self.velocity += self.resultingAcc * duration    # update velocity
        self.velocity *= pow(self.damping, duration)
        
        self.clearAccumulator()
        
    
    # =================================================================
    def clearAccumulator(self):
        self.forceAccum = np.zeros(3)
    
    def addForce(self, force):
        self.forceAccum += force
        
        
class ParticleForceGenerator(object):
    def updateForce(self, particle, duration):
        pass


        

if __name__ == "__main__":
    p = Particle()
    p.setMass(1.0)
    p.setDamping(0.99)
    p.setPosition((0., 0., 0.))
    p.setVelocity((4., 10., 0.))
    p.setAcceleration((0., 0., 0.))
    
    p.forceAccum += GRAVITY * p.mass
    
    from time import time
    import matplotlib.pyplot as plt


    def time_ms():
        return int(round(time() * 1000))


    t = time_ms()

    trajectory = []
    for _ in range(1000):
        p.integrate(0.01)
        trajectory.append([p.position[0], p.position[1]])

    print("time: ", time_ms() - t, "ms")
    
    plt.plot(*zip(*trajectory))
    plt.show()
    
    
 
