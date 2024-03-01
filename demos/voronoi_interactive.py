import moderngl
import numpy as np
import torch

from test_cases import Cases
from wXyEngine import TORCH_DEVICE
from wXyEngine.Interface.interface import (
    SimpleInterfaceInteractive,
)
from wXyEngine.Renderer.mdgl_utils import Transform2d
from wXyEngine.Utils.sampling import Boundary
from wXyEngine.Utils.optimize_utils import (
    set_points_to_groups,
    map_indices,
)

MULTI_SITES = False
DEVICE = TORCH_DEVICE
p = 2**0

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
        self.nodes = torch.empty((0, 2), device=DEVICE)
        self.weight = torch.empty((0, 1), device=DEVICE)
        self.edges = []
        self.adj = {}

    def add_node(self, node, weight=1.0):
        self.nodes = torch.cat(
            (
                self.nodes,
                torch.tensor([node], device=DEVICE),
            )
        )
        # self.weight = torch.append(self.weight, torch.tensor([weight]))

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
        site_new[i] = torch.mean(sample_points[sp_site_idx == i], dim=0)
    return site_new


# TODO: use shader to compute(sp2group, etc.) and draw voronoi diagram
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

        # imgui.create_context()
        # self.wnd.ctx.error
        # self.imgui = ModernglWindowRenderer(self.wnd)

        global voronoi
        self.voronoi = voronoi

        self.transform = Transform2d(scale=[0.12, 0.12], offset=[0, 0])
        self.prog["transform"].value = self.transform.mat3.flatten().astype(
            "f4"
        )
        self.particle_prog["transform"].value = (
            self.transform.mat3.flatten().astype("f4")
        )

        self.sp = boundary.sample_inside(n=20000, inplace=False, device=DEVICE)
        self.sp_site_idx = set_points_to_groups(
            self.sp, voronoi.sites, p=p, device=DEVICE
        )
        if MULTI_SITES:
            self.sp_site_idx = map_indices(
                self.sp_site_idx, voronoi.site_group_idx
            )

    def mouse_press_event(self, x, y, button):
        global MULTI_SITES
        if button == 1:
            fixed_x, fixed_y = self.map_wnd_to_gl(x, y)
            transformed_xy = self.transform.inv_mat3 @ np.array([
                fixed_x, fixed_y, 1
            ])
            voronoi.diagram.add_node([transformed_xy[0], transformed_xy[1]])
        if button == 2:
            MULTI_SITES = not MULTI_SITES
            print(f"MULTI_SITES: {MULTI_SITES}")

        voronoi.refresh_groups()
        self.sp_site_idx = set_points_to_groups(
            self.sp, voronoi.sites, p=p, device=DEVICE
        )

        if MULTI_SITES:
            self.sp_site_idx = map_indices(
                self.sp_site_idx, voronoi.site_group_idx
            )

    # def key_event(self, key: Any, action: Any, modifiers: KeyModifiers):
    #     keys = self.wnd.keys
    #
    #     if action == keys.ACTION_PRESS:
    #         print(f"key: {key}")
    #
    #     if key != 122:  # z
    #         return

    def lloyd_relaxation(self):
        voronoi.sites = Lloyd_relaxation(
            voronoi.sites,
            self.sp,
            set_points_to_groups(self.sp, voronoi.sites, p=p, device=DEVICE),
        )

        self.sp_site_idx = set_points_to_groups(
            self.sp, voronoi.sites, p=p, device=DEVICE
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
        if self.wnd.is_key_pressed(122):  # z
            print("==Lloyd Relaxation==")
            self.lloyd_relaxation()

        # ---draw---
        self.draw_grid(scale=10, color=np.array([0.9, 0.9, 0.9]))
        self.draw_polygon(voronoi.boundary.vtx2xy, np.array([0, 0, 0]))

        self.draw_particles(
            self.sp.cpu(),
            self.sp_site_idx.cpu(),
            point_size=6,
            # use_circle=False,
        )
        self.draw_particles(
            voronoi.diagram.nodes.cpu(),
            point_size=16,
            # use_circle=False,
        )

        if MULTI_SITES:
            self.draw_particles(
                voronoi.sites.cpu(),
                voronoi.site_group_idx.cpu(),
                point_size=12,
                use_circle=False,
            )


if __name__ == "__main__":
    use_case = 5
    vtx = Cases.boundary_vtx[use_case] - np.mean(
        Cases.boundary_vtx[use_case], axis=0
    )

    boundary = Boundary(vtx * 1.2 * 10)

    # --------------------------------------------------------------------------
    dgm = Diagram()
    dgm.add_node([0, 0])
    # dgm.add_node([0, -4])
    # dgm.add_node([-3, 3])
    # dgm.add_node([0, 0])
    # dgm.add_node([3, 3])
    # dgm.add_edge(0, 1)
    # dgm.add_edge(1, 2)
    # --------------------------------------------------------------------------

    voronoi = Voronoi(dgm, boundary)
    # plt_draw(voronoi)
    Draw.run()
