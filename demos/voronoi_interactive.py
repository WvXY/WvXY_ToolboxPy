import moderngl
import numpy as np
import torch
from test_cases import Cases

from pymrt import TORCH_DEVICE
from pymrt.Interface.interface import (
    SimpleAppInteractive,
)
from pymrt.Renderer.utils import Transform2d, generate_grids
from pymrt.Utils.optimize_utils import (
    set_points_to_groups,
    map_indices,
)
from voronoi import Voronoi
from pymrt.Utils.sampling import Boundary


class VoronoiDemoApp(SimpleAppInteractive):
    gl_version = (4, 6)
    title = "Interactive Voronoi Demo"
    vsync = True
    window_size = (800, 800)
    aspect_ratio = window_size[0] / window_size[1]
    resizable = False
    resampling = 4

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.boundary = Boundary(Cases.boundary_vtx[1])
        self.voronoi = Voronoi(boundary=self.boundary)
        self.init_voronoi()

        self.transform2 = None
        self.set_uniforms()
        self.grid = None

        # self.sp = boundary.sample_inside(n=10000, inplace=False, device=TORCH_DEVICE)
        # self.sp_site_idx = set_points_to_groups(
        #     self.sp,
        #     voronoi.sites[:, :2],
        #     p=p,
        #     device=TORCH_DEVICE,
        #     weight=voronoi.sites[:, 2],
        # )

    @property
    def seeds(self):
        return self.voronoi.seeds

    def set_uniforms(self):
        self.transform2 = Transform2d()
        self.transform2.scale(0.12, 0.12)
        self.particle_system.set_uniform(
            "transform3", self.transform2.mat3.flatten("F")
        )
        self.basic_system.set_uniform(
            "transform3", self.transform2.mat3.flatten("F")
        )
        self.voronoi_system.set_uniform(
            "transform3", self.transform2.mat3.flatten("F")
        )
        self.voronoi_system.set_uniform(
            "transform3Inv", self.transform2.inv_mat3.flatten("F")
        )

    def init_voronoi(self):
        self.voronoi.set_experimental_mode(1)
        self.voronoi.generate_seeds_inside_boundary(n_seeds=100)

    def mouse_press_event(self, x, y, button):
        if button == 1:
            fixed_x, fixed_y = self.map_wnd_to_gl(x, y)
            transformed_xy = self.transform2.inv_mat3 @ np.array(
                [fixed_x, fixed_y, 1]
            )
            self.voronoi.add_seed(
                [transformed_xy[0], transformed_xy[1], torch.rand(1) + 1]
            )

        # voronoi.refresh_groups()
        # self.sp_site_idx = set_points_to_groups(
        #     self.sp,
        #     self.voronoi.seeds[:, :2],
        #     p=p,
        #     device=TORCH_DEVICE,
        #     # weight=voronoi.sites[:, 2],
        # )

    def render(self, time: float, frame_time: float, **kwargs):
        self.ctx.clear(0.8, 0.8, 0.8)
        self.ctx.enable(
            moderngl.BLEND
            | moderngl.PROGRAM_POINT_SIZE  # | moderngl.DEPTH_TEST
        )

        # ---draw---
        self.grid = (
            generate_grids(n=10) * 10 if self.grid is None else self.grid
        )
        self.basic_system.draw_grid(
            grid=self.grid, color=np.array([0.9, 0.9, 0.9])
        )

        self.voronoi.seeds[0, 2] = torch.sin(torch.tensor(time)) + 1
        self.voronoi.seeds[1, 2] = torch.cos(torch.tensor(time * 0.5 + 1)) + 1
        self.voronoi.seeds[2, 2] = torch.sin(torch.tensor(time * 0.3 + 1)) + 1
        # voronoi.sites[0, 2] += 0.005
        # print(voronoi.sites[0, 2])

        self.voronoi_system.create_buffer(
            self.voronoi.seeds[:, :3].cpu(), self.boundary.vtx2xy
        )

        for site in self.voronoi.seeds.cpu():
            self.particle_system.create_buffer(
                [site[:2]],
                point_size=site[2] * 10,
            )

        self.voronoi_system.draw()
        self.particle_system.draw()


if __name__ == "__main__":
    VoronoiDemoApp.voronoi.add_seed([0, 0, 1])
    VoronoiDemoApp.voronoi.add_seed([1, 0, 1])

    VoronoiDemoApp.run()
