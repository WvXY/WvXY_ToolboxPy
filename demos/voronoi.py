import torch

from pymrt.Utils.sampling import Boundary


use_case = 1
p = 2**1

# if p == 1:
#     print("Using manhattan distance")
# elif p == 2:
#     print("Using euclidean distance")
# elif p >= 16:  # 2^4
#     print("Using chebyshev distance")
# else:
#     print(f"Using minkowski distance with p={p}")


class Voronoi:
    def __init__(
        self,
        seeds=None,
        n_seeds=16,
        boundary: Boundary = None,
    ):
        self.seeds = seeds
        self.n_seeds = len(seeds) if seeds is not None else n_seeds
        self.boundary = boundary

        self._experimental_mode = 0
        self._seed_dim = 2

    def generate_seeds_inside_boundary(self, boundary=None, n_seeds=None):
        if boundary is None:
            boundary = self.boundary
        if n_seeds is None:
            n_seeds = self.n_seeds
        self.seeds = boundary.sample_inside(n=n_seeds, inplace=False)
        if self._experimental_mode:
            self.seeds = torch.cat(
                [self.seeds, torch.ones(n_seeds, self._experimental_mode)],
                dim=1,
            )

    # experimental feature
    def set_experimental_mode(self, exp_mode=0):
        """exp_mode =
        0 for normal [x, y] seeds,
        1 for [x, y, w] seeds,
        2 for [x, y, w, z] seeds
        """
        assert self.seeds is not None
        self._experimental_mode = exp_mode
        self._seed_dim = 2 + exp_mode

    def add_seed(self, seed):
        self.seeds = torch.cat([self.seeds, seed])

    @property
    def sample_points(self):
        return self.boundary.sample_points

    @property
    def seed_dim(self):
        assert self.seeds.shape[1] == self._seed_dim
        return self._seed_dim

    def distance(self, xy, idx):
        return torch.norm(xy - self.seeds[idx])

    def distance_to_all_seeds(self, xy):
        return torch.norm(xy - self.seeds, dim=1)

    @staticmethod
    def lloyd_relaxation(
        seeds: torch.Tensor,
        sample_points: torch.Tensor,
        sp_seed_idx=None,
    ):
        seeds = seeds.clone().detach()
        seed_new = torch.zeros_like(seeds, device=DEVICE)
        sample_points = sample_points.clone().detach()
        sp_seed_idx = sp_seed_idx.clone().detach()
        for i, seed in enumerate(seeds):
            seed_new[i, :2] = (
                torch.mean(sample_points[sp_seed_idx == i], dim=0)
                if len(sample_points[sp_seed_idx == i]) > 0
                else seed[:2]
            )
            seed_new[i, 2] = seed[2]
        return seed_new


class MultiGroupVoronoi(Voronoi):
    def __init__(self):
        super().__init__()
        self.groups = []
        self.groupInfo = {}
