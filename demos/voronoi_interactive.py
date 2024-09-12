import moderngl
import numpy as np
import torch
from torch import dtype

from test_cases import Cases

from w_tbx import TORCH_DEVICE
from w_tbx.Interface.interface import (
    SimpleAppInteractive,
)
from w_tbx.Renderer.utils import Transform2d, generate_grids
from w_tbx.Utils.optimize_utils import (
    set_points_to_groups,
    map_indices,
)
from w_tbx.Geometry import Voronoi
from w_tbx.Utils.sampling import Boundary


class VoronoiDemoApp(SimpleAppInteractive):
    gl_version = (4, 6)
    title = "Interactive Voronoi Demo"
    vsync = False
    window_size = (1280, 720)
    aspect_ratio = window_size[0] / window_size[1]
    resizable = False
    resampling = 4

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.i_case = 1
        self.__bvtx = Cases.boundary_vtx[self.i_case] - np.mean(
            Cases.boundary_vtx[self.i_case], axis=0
        )
        self.boundary = Boundary(self.__bvtx * 1.2 * 10)
        self.voronoi = Voronoi(boundary=self.boundary)
        self.voronoi_mode = 0
        self.init_voronoi()

        self.transform2 = None
        self.set_uniforms()
        self.grid = None

        del self.__bvtx

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
        self.voronoi_system.set_uniform(
            "resolution",
            np.array((self.wnd.width, self.wnd.height), dtype="f4"),
        )
        self.voronoi_system.set_uniform(
            "vMode", self.voronoi_mode.to_bytes(4, "little")
        )

    def init_voronoi(self):
        self.voronoi.set_experimental_mode(0)
        # self.voronoi.generate_seeds_inside_boundary(n_seeds=10)
        self.voronoi.add_seed([0, 0, 0.0, 0.0])
        # self.voronoi.add_seed([0, 0, 0.5, 0.5])

    def mouse_press_event(self, x, y, button):
        if button == 1:
            fixed_x, fixed_y = self.map_wnd_to_gl(x, y)
            transformed_xy = self.transform2.inv_mat3 @ np.array(
                [fixed_x, fixed_y, 1]
            )
            self.voronoi.add_seed(
                [
                    transformed_xy[0],
                    transformed_xy[1],
                    torch.rand(1) * 0.5 + 0.5,
                    torch.rand(1) * 0.5 + 0.5,
                ]
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
            moderngl.BLEND | moderngl.PROGRAM_POINT_SIZE | moderngl.DEPTH_TEST
        )

        # ---draw---
        self.grid = (
            generate_grids(n=10) * 10 if self.grid is None else self.grid
        )
        self.basic_system.draw_grid(
            grid=self.grid, color=np.array([0.9, 0.9, 0.9])
        )

        # self.voronoi.seeds[0, 2] = torch.sin(torch.tensor(time))
        # self.voronoi.seeds[0, 3] = torch.cos(torch.tensor(time * 0.5 + 1))
        # self.voronoi.seeds[2, 2] = torch.sin(torch.tensor(time * 0.3 + 1)) + 1
        # voronoi.sites[0, 2] += 0.005
        # print(voronoi.sites[0, 2])

        self.voronoi_system.create_buffer(
            self.voronoi.seeds[:, :].cpu(), self.boundary.vtx2xy
        )

        for site in self.voronoi.seeds.cpu():
            self.particle_system.create_buffer(
                [site[:2]],
                point_size=site[2] * 10,
            )

        self.voronoi_system.draw()
        self.particle_system.draw()


if __name__ == "__main__":
    VoronoiDemoApp.run()
