from src/PyGameEngine import PyGameEngine

class ParticleTest(PyGameEngine):
    p = PyGameEngine.Particle()
    p.setMass(1.0)
    p.setDamping(0.99)
    p.setPosition((0., 0., 0.))
    p.setVelocity((4., 100., 0.))
    p.setAcceleration((0., 0., 0.))
    

ParticleTest().run()
#     for i in range(100):

