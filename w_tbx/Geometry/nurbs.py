import numpy as np


class NURBS:
    def __init__(self, control_points, weight, knot_vector, degree):
        self.p = degree
        self.W = weight
        self.U = knot_vector
        self.P = control_points
        self.n = len(self.P)

    def __basis_function(self, t, i, p):
        if p == 0:
            if self.U[i] <= t < self.U[i + 1]:
                return 1
            else:
                return 0
        else:  # can be optimized
            B1 = self.__basis_function(t, i, p - 1)
            B2 = self.__basis_function(t, i + 1, p - 1)
            if B1 == 0:
                N1 = 0
            else:
                N1 = B1 * (t - self.U[i]) / (self.U[i + p] - self.U[i])
            if B2 == 0:
                N2 = 0
            else:
                N2 = B2 * (self.U[i + p + 1] - t) / (self.U[i + p + 1] - self.U[i + 1])
            # l1 = (t - U[i]) / (U[i+p] - U[i])
            # l2 = (U[i+p+1] - t) / (U[i+p+1] - U[i+p])

            # return basis_function(t, i, p-1, U) * l1 + \
            #    basis_function(t, i+1, p-1, U)* l2
            return N1 + N2

    def __rational_basis_function(self, t, i, p):
        sum = 0
        for j in range(self.n):
            sum += self.W[j] * self.__basis_function(t, j, p)
        return self.__basis_function(t, i, p) * self.W[i] / sum

    def get_pos(self, t):
        pos = np.zeros([1, 2])
        for i in range(self.n):
            pos += self.__rational_basis_function(t, i, self.p) * self.P[i]
        return pos
