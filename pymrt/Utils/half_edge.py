import numpy as np

from ..Geometry.mesh import Mesh


class Vertex:
    __vid = 0

    def __init__(self, xy, idx=None):
        self.idx = idx
        self.xy = xy
        self.next = []
        self.prev = []

        self.edges = None
        self.faces = []
        self.border = False
        self.vid = Vertex.__vid
        Vertex.__vid += 1

    @property
    def x(self):
        return self.xy[0]

    @property
    def y(self):
        return self.xy[1]

    def move(self, dx, dy) -> None:
        if self.border:
            return
        xy_old = self.xy.copy()
        self.xy += [dx, dy]
        for f in self.faces:
            if f.flipped:
                self.xy = xy_old
                return


class HalfEdge:
    def __init__(self, origin, to):
        self.origin = origin
        self.to = to
        self.face = None
        self.twin = None
        self.next = None
        self.prev = None

    @property
    def outside(self):
        return not self.twin

    @property
    def gid(self):
        return self.face.gid

    def dir(self):
        return (self.to.xy - self.origin.xy) / self.length()

    def orth(self):
        return np.array([dir[1], -dir[0]])

    def length(self):
        return np.linalg.norm(self.to.xy - self.origin.xy)


class Face:
    def __init__(self):
        self.nodes = []
        self.gid = 0
        self.half_edges = []

    @property
    def area(self):
        area = 0
        for i in range(3):
            j = (i + 1) % 3
            area += (
                    self.nodes[i].x * self.nodes[j].y
                    - self.nodes[j].x * self.nodes[i].y
            )
        return area / 2

    @property
    def flipped(self):
        return self.area < 0

    @property
    def adj_faces(self):
        adj_faces = []
        for e in self.half_edges:
            if e.twin:
                adj_faces.append(e.twin.face)
        return adj_faces


class HalfEdgeManager:
    def __init__(self):
        self.faces = []
        self.edges = []
        self.nodes = []  # =vertices (keep same var length as edges and faces)

        self.visited = [False] * len(self.nodes)

    @property  # alias
    def vertices(self):
        return self.nodes

    def from_mesh(self, mesh: Mesh):
        self.clear()

        # nodes
        for i, xy in enumerate(mesh.nodes):
            self.nodes.append(Vertex(xy, i))

        # faces
        for i, f in enumerate(mesh.faces):
            face = Face()
            face.nodes = [
                self.nodes[f[0]],
                self.nodes[f[1]],
                self.nodes[f[2]],
            ]
            self.faces.append(face)

            for j in f:
                self.nodes[j].faces.append(face)

        # half-edges
        for i, (fi, fj, fk) in enumerate(mesh.faces):
            # prev i - k - j - i
            self.nodes[fi].prev.append(self.nodes[fk])
            self.nodes[fj].prev.append(self.nodes[fi])
            self.nodes[fk].prev.append(self.nodes[fj])
            # next i - j - k - i
            self.nodes[fi].next.append(self.nodes[fj])
            self.nodes[fj].next.append(self.nodes[fk])
            self.nodes[fk].next.append(self.nodes[fi])

            eij = HalfEdge(self.nodes[fi], self.nodes[fj])
            ejk = HalfEdge(self.nodes[fj], self.nodes[fk])
            eki = HalfEdge(self.nodes[fk], self.nodes[fi])

            eij.next, ejk.next, eki.next = ejk, eki, eij
            eij.prev, ejk.prev, eki.prev = eki, eij, ejk
            eij.face, ejk.face, eki.face = (
                self.faces[i],
                self.faces[i],
                self.faces[i],
            )

            self.edges += [eij, ejk, eki]
            self.faces[i].half_edges = [eij, ejk, eki]

        # finalize
        self.get_twin()
        self.get_nodes_info()

    def get_twin(self):
        n = len(self.edges)
        for i in range(n):
            ei = self.edges[i]
            if ei.twin:
                continue

            for j in range(i + 1, n):
                ej = self.edges[j]
                if ej.twin:
                    continue

                if ei.origin == ej.to and ei.to == ej.origin:
                    ei.twin, ej.twin = ej, ei

    def get_nodes_info(self):
        for e in self.edges:
            if e.twin is None:
                self.nodes[e.origin.idx].border = True
                self.nodes[e.to.idx].border = True

    def clear(self):
        self.faces.clear()
        self.edges.clear()
        self.nodes.clear()
