from wXyEngine.Geometry import GameObjectManager, SdParticle, SdRectangle
from wXyEngine.Interface.interface import SimpleInterface

import torch
import moderngl

gom = GameObjectManager()
for i in range(10):
    gom.add(SdParticle(torch.rand(2) * 100))
    gom.game_objects[i].color = torch.rand(3)
    gom.game_objects[i].velocity = torch.rand(2) * 10 - 5

border = SdRectangle([50, 50], 100, 100)

class ParticleDemo(SimpleInterface):
    resizable = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mb_prog = self.ctx.program(
            '''
            #version 330
            
            uniform float point_size;
            
            in vec2 in_position;
            
            '''
        )

    def render(self, time: float, frame_time: float):
        self.ctx.clear(1.0, 1.0, 1.0)
        self.ctx.enable(moderngl.BLEND | moderngl.PROGRAM_POINT_SIZE)

        gom.update()
        self.draw_particles(gom.get_position(), gom.get_color())
        border.draw(self.ctx)

