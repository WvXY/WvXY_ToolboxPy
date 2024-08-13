import numpy as np


class Mesh:
    """Mesh class and mesh utilities"""

    def __init__(self, v=None, f=None):
        self.faces = f
        self.nodes = v

    @property
    def vertices(self):
        return self.nodes

    @property
    def edges(self, add_reverse=True):
        return self.face2edge(self.faces, add_reverse=add_reverse)

    def generate_mesh_from_polygon(self, polygon, mesh_size=0.2, lib="pygmsh", **kwargs):
        """
        Generate mesh from polygon
        :param polygon: 2d array of vertices
        :param mesh_size: mesh size
        :param lib: library to use (pygmsh, pygalmesh, del_msh)
        :param kwargs: additional arguments for pygalmesh
        """
        vertices = np.array(polygon, dtype=np.float32)
        if lib == "pygmsh":
            v, f = self._gmsh_gen(vertices, mesh_size)
        elif lib == "pygalmesh":
            v, f = self._pygalmesh_gen(vertices, mesh_size, **kwargs)
        elif lib == "del_msh":
            from del_msh import PolyLoop

            boundary_size = kwargs.get("boundary_size", mesh_size)
            f, v = PolyLoop.tesselation2d(
                vertices.astype("f4"),
                boundary_size,
                mesh_size,
            )
        else:
            print(f"lib: {lib} is not supported")
            raise NotImplementedError

        self.faces, self.nodes = f, v

    @staticmethod
    def _gmsh_gen(polygon, mesh_size):
        import pygmsh

        with pygmsh.geo.Geometry() as geom:
            geom.add_polygon(
                polygon,
                mesh_size=mesh_size,
            )
            mesh = geom.generate_mesh()

        return mesh.points, mesh.cells_dict["triangle"]

    @staticmethod
    def _pygalmesh_gen(
            polygon,
            mesh_size,
            indices=None,
            num_lloyd_steps=10,
            **kwargs,
    ):
        import pygalmesh

        if indices is None:
            n_vertices = polygon.shape[0]
            indices_range = np.arange(0, n_vertices)
            indices = np.vstack([
                indices_range,
                np.roll(indices_range, -1, axis=0),
            ]).T

        mesh = pygalmesh.generate_2d(
            polygon,
            constraints=indices,
            max_edge_size=mesh_size,
            num_lloyd_steps=num_lloyd_steps,
        )

        # Problem: pygalmesh does not support 2d mesh output
        # import meshio
        # meshio.write_points_cells(
        #     "mesh.obj",
        #     mesh.points,
        #     [("triangle", mesh.cells_dict["triangle"])],
        # )
        #
        # mesh = pygalmesh.remesh_surface(
        #     "mesh.obj",
        #     max_edge_size_at_feature_edges=0.025,
        #     min_facet_angle=25,
        #     max_radius_surface_delaunay_ball=0.1,
        #     max_facet_distance=0.001,
        #     verbose=False,
        # )

        return mesh.points, mesh.cells_dict["triangle"]

    @staticmethod
    def face2edge(faces, add_reverse=False):
        """return undirected edges from faces"""
        edges = []
        faces = np.sort(np.array(faces, dtype=np.int32), axis=1)
        for f in faces:
            edges.append([f[0], f[1]])
            edges.append([f[1], f[2]])
            edges.append([f[0], f[2]])
        edges = np.unique(np.array(edges), axis=0)
        if add_reverse:
            edges = np.vstack((edges, np.flip(edges, axis=1)))
        return edges
