import moderngl
import numpy as np
import torch

from test_cases import Cases
from pymrt import TORCH_DEVICE
from pymrt.Interface.interface import (
    SimpleInterfaceInteractive,
)
from pymrt.Renderer.mdgl_utils import Transform2d
from pymrt.Utils.sampling import Boundary
from pymrt.Utils.optimize_utils import (
    set_points_to_groups,
    map_indices,
)

MULTI_SITES = False
DEVICE = TORCH_DEVICE
use_case = 5
p = 2**1

if p == 1:
    print("Using manhattan distance")
elif p == 2:
    print("Using euclidean distance")
elif p >= 16:  # 2^4
    print("Using chebyshev distance")
else:
    print(f"Using minkowski distance with p={p}")


# --------------------------------------------------------------------------
class Diagram:  # TODO: optimize this / better structure
    def __init__(self):
        self.nodes = torch.empty((0, 3), device=DEVICE)  # [x, y, w]
        self.edges = []
        self.adj = {}

    def add_node(self, node):
        self.nodes = torch.cat(
            (
                self.nodes,
                torch.tensor([node], device=DEVICE),
            )
        )

    def add_edge(self, i, j):
        self.edges.append([i, j])
        self.adj[i] = j
        self.adj[j] = i


class Group:
    __group_id = 0

    def __init__(self, r_type):
        self.idx_sites = []
        self.type = r_type  # use groupInfo to change it
        self.group_id = Group.__group_id
        Group.__group_id += 1

    def add_site_idx(self, idx):
        self.idx_sites.append(idx)


class Voronoi:
    def __init__(
        self,
        bubble_diagram: Diagram,
        boundary: Boundary,
    ):
        self.diagram = bubble_diagram
        self.n_sites = bubble_diagram.nodes.shape[0] * 5
        self.boundary = boundary

        self.groups, self.sites, self.site_group_idx = (
            None,
            None,
            None,
        )
        self.refresh_groups()

    @staticmethod
    def create_sites(boundary, n_sites):
        return boundary.sample_inside(n=n_sites, inplace=False)

    def set_multisite_groups(self):
        for s_idx, r_idx in enumerate(self.site_group_idx):
            self.groups[r_idx].add_site_idx(s_idx)

    def refresh_groups(self):
        self.groups = [Group(_i) for _i in range(len(self.diagram.nodes))]
        self.n_sites = self.diagram.nodes.shape[0] * 6
        self.sites = self.diagram.nodes

        if MULTI_SITES:
            self.sites = self.create_sites(self.boundary, self.n_sites)
            self.site_group_idx = set_points_to_groups(
                self.sites,
                self.diagram.nodes,
                p=p,
                device=DEVICE,
            )
            self.set_multisite_groups()

    @property
    def sample_points(self):
        return self.boundary.sample_points

    def distance(self, xy, idx):
        return torch.norm(xy - self.sites[idx].center)

    def distance_to_all_sites(self, xy):
        return torch.norm(xy - self.sites, dim=1)


def Lloyd_relaxation(
    sites: torch.Tensor,
    sample_points: torch.Tensor,
    sp_site_idx=None,
):
    sites = sites.clone().detach()
    site_new = torch.zeros_like(sites, device=DEVICE)
    sample_points = sample_points.clone().detach()
    sp_site_idx = sp_site_idx.clone().detach()
    for i, site in enumerate(sites):
        site_new[i, :2] = (
            torch.mean(sample_points[sp_site_idx == i], dim=0)
            if len(sample_points[sp_site_idx == i]) > 0
            else site[:2]
        )
        site_new[i, 2] = site[2]
    return site_new


class Draw(SimpleInterfaceInteractive):
    gl_version = (4, 6)
    title = "Interactive Voronoi Demo"
    vsync = False
    window_size = (800, 800)
    aspect_ratio = window_size[0] / window_size[1]
    resizable = True
    resampling = 4

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        global voronoi
        self.voronoi = voronoi

        self.tsfm = Transform2d()
        self.tsfm.scale(0.12, 0.12)
        self.prog["transform"].value = self.tsfm.mat3.flatten(order="F")
        self.particle_prog["transform"].value = self.tsfm.mat3.flatten("F")
        # self.voronoi_prog["transform"].write(
        #     self.tsfm.mat3.flatten("F").tobytes()
        # )
        self.voronoi_system.set_uniform("transform", self.tsfm.mat3.flatten("F"))

        self.sp = boundary.sample_inside(n=10000, inplace=False, device=DEVICE)
        self.sp_site_idx = set_points_to_groups(
            self.sp,
            voronoi.sites[:, :2],
            p=p,
            device=DEVICE,
            weight=voronoi.sites[:, 2],
        )
        if MULTI_SITES:
            self.sp_site_idx = map_indices(
                self.sp_site_idx, voronoi.site_group_idx
            )

    def mouse_press_event(self, x, y, button):
        global MULTI_SITES
        if button == 1:
            fixed_x, fixed_y = self.map_wnd_to_gl(x, y)
            transformed_xy = self.tsfm.inv_mat3 @ np.array([
                fixed_x, fixed_y, 1
            ])
            voronoi.diagram.add_node([
                transformed_xy[0], transformed_xy[1], torch.rand(1) + 1
            ])
        # if button == 2:
        #     MULTI_SITES = not MULTI_SITES
        #     print(f"MULTI_SITES: {MULTI_SITES}")

        voronoi.refresh_groups()
        self.sp_site_idx = set_points_to_groups(
            self.sp,
            voronoi.sites[:, :2],
            p=p,
            device=DEVICE,
            # weight=voronoi.sites[:, 2],
        )

        if MULTI_SITES:
            self.sp_site_idx = map_indices(
                self.sp_site_idx, voronoi.site_group_idx
            )

    def lloyd_relaxation(self):
        voronoi.sites = Lloyd_relaxation(
            voronoi.sites,
            self.sp,
            set_points_to_groups(
                self.sp,
                voronoi.sites[:, :2],
                p=p,
                device=DEVICE,
                # weight=voronoi.sites[:, 2],
            ),
        )

        self.sp_site_idx = set_points_to_groups(
            self.sp,
            voronoi.sites[:, :2],
            p=p,
            device=DEVICE,
            # weight=voronoi.sites[:, 2],
        )

        if MULTI_SITES:
            # voronoi.diagram.nodes = Lloyd_relaxation(
            #     voronoi.diagram.nodes, voronoi.sites, voronoi.site_group_idx
            # )

            self.sp_site_idx = map_indices(
                self.sp_site_idx, voronoi.site_group_idx
            )
        else:
            voronoi.diagram.nodes = voronoi.sites

    def render(self, time: float, frame_time: float, **kwargs):
        self.ctx.clear(0.8, 0.8, 0.8)
        self.ctx.enable(
            moderngl.BLEND
            | moderngl.PROGRAM_POINT_SIZE  # | moderngl.DEPTH_TEST
        )

        # ---optimize---
        # if self.wnd.is_key_pressed(122):  # z
        #     print("==Lloyd Relaxation==")
        #     self.lloyd_relaxation()
        #
        # for i in range(voronoi.sites.shape[0]):
        #     voronoi.sites[i, 2] = torch.sin(torch.tensor(time + i * 3)) * 4
        # voronoi.refresh_groups()
        # self.sp_site_idx = set_points_to_groups(
        #     self.sp,
        #     voronoi.sites[:, :2],
        #     p=p,
        #     device=DEVICE,
        #     # weight=voronoi.sites[:, 2],
        # )
        # self.lloyd_relaxation()

        # ---draw---
        self.draw_grid(scale=10, color=np.array([0.9, 0.9, 0.9]))

        # for site in voronoi.sites.cpu():
        #     site[2] = 1 + torch.sin(torch.tensor(site[2] + time))
        voronoi.sites[0, 2] = torch.sin(torch.tensor(time)) + 1

        self.voronoi_system.draw(voronoi.sites[:, :3].cpu(), voronoi.boundary.vtx2xy)

        # self.draw_particles(
        #     voronoi.sites.cpu()[..., :2],
        #     point_size=voronoi.sites.cpu()[:, 2] * 100,
        #     # use_circle=False,
        # )
        for site in voronoi.sites.cpu():
            self.draw_particles(
                [site[:2]],
                point_size=site[2] * 20,
            )

        # if MULTI_SITES:
        #     self.draw_particles(
        #         voronoi.sites.cpu(),
        #         voronoi.site_group_idx.cpu(),
        #         point_size=12,
        #         use_circle=False,
        #     )


if __name__ == "__main__":
    vtx = Cases.boundary_vtx[use_case] - np.mean(
        Cases.boundary_vtx[use_case], axis=0
    )
    boundary = Boundary(vtx * 1.2 * 10)
    # --------------------------------------------------------------------------
    dgm = Diagram()
    dgm.add_node([0, 0, 0])
    # --------------------------------------------------------------------------
    voronoi = Voronoi(dgm, boundary)
    Draw.run()
