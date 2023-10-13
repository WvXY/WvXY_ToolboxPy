import numpy as np


class ParticleForceGenerator:
    def updateForce(particle, duration):
        pass



class ParticleGravity(ParticleForceGenerator):
    gravity = np.array([0.0, -9.8, 0.0], dtype="f4")    # earth gravity



class ParticleForceRegistration:
    def __init__(self, particle, fg):
        self.particle = particle
        self.fg = fg

    def add(self):
        pass

    def remove(self):
        pass

    def clear(self):
        pass

    def updateForces(self, duration):
        for i in range(N):
            self.fg.updateForce(self.particle[i], duration)







        