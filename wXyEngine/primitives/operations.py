import numpy as np


# boolean operations
def sdUnion(a, b):
    return np.minimum(a, b)


def sdIntersection(a, b):
    return np.maximum(a, b)


def sdDifference(a, b):
    return np.maximum(a, -b)


def sdComplement(a):
    return -a


def sdAdd(a, b):
    return a + b


# --------------------------------------------------------------------------------------------
# fast sweeping method
# @jit(nopython=True)
def fast_sweeping(f, h, max_iter, tol, boundary_cond):
    u = f.copy()
    delta_u = np.inf
    iter = max_iter

    while delta_u > tol and iter > 0:
        delta_u = 0
        iter -= 1

        # Sweep in the up direction
        for i in range(1, u.shape[0]):
            for j in range(u.shape[1]):
                if boundary_cond == "dirichlet":
                    u[i, j] = min(u[i, j], u[i - 1, j] + h)
                elif boundary_cond == "neumann":
                    u[i, j] = min(u[i, j], u[i - 1, j] + h / 2)
                delta_u = max(delta_u, abs(u[i, j] - f[i, j]))

        # Sweep in the down direction
        for i in range(u.shape[0] - 2, -1, -1):
            for j in range(u.shape[1]):
                if boundary_cond == "dirichlet":
                    u[i, j] = min(u[i, j], u[i + 1, j] + h)
                elif boundary_cond == "neumann":
                    u[i, j] = min(u[i, j], u[i + 1, j] + h / 2)
                delta_u = max(delta_u, abs(u[i, j] - f[i, j]))

        # Sweep in the left direction
        for i in range(u.shape[0]):
            for j in range(1, u.shape[1]):
                if boundary_cond == "dirichlet":
                    u[i, j] = min(u[i, j], u[i, j - 1] + h)
                elif boundary_cond == "neumann":
                    u[i, j] = min(u[i, j], u[i, j - 1] + h / 2)
                delta_u = max(delta_u, abs(u[i, j] - f[i, j]))

        # Sweep in the right direction
        for i in range(u.shape[0]):
            for j in range(u.shape[1] - 2, -1, -1):
                if boundary_cond == "dirichlet":
                    u[i, j] = min(u[i, j], u[i, j + 1] + h)
                elif boundary_cond == "neumann":
                    u[i, j] = min(u[i, j], u[i, j + 1] + h / 2)
                delta_u = max(delta_u, abs(u[i, j] - f[i, j]))

    return u


# marching square
class MarchingSquare:
    def __init__(self, grid, threshold=0.0):
        self.grid = grid
        self.threshold = threshold

    def get_square(self, i, j):
        return self.grid[i : i + 2, j : j + 2]

    def get_square_value(self, i, j):
        return self.get_square(i, j).flatten()

    def get_square_sign(self, i, j):
        return np.sign(self.get_square_value(i, j) - self.threshold)

    def get_square_index(self, i, j):
        return np.array([[i, j], [i + 1, j], [i + 1, j + 1], [i, j + 1]])

    def find_intersection(self, p, q, F):
        pq2 = (p + q) / 2.0
        Fpq = F(pq2)
        if abs(Fpq) < 1e-6:
            return pq2
        elif Fpq > 0:
            return self.find_intersection(p, pq2, F)
        else:
            return self.find_intersection(pq2, q, F)

    def marching(self):
        N = self.grid.shape[0]
        points = []
        for i in range(N - 1):
            for j in range(N - 1):
                signs = self.get_square_sign(i, j)
                if np.all(signs == 1) or np.all(signs == -1):
                    continue
                else:
                    index = self.get_square_index(i, j)
                    pass
        return np.array(points)

