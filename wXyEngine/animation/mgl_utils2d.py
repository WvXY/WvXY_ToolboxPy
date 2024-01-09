import moderngl
import numpy as np


# some drawing functions
class MglUtil2d:
    def __init__(self):
        self.prog = None
        self.particle_prog = None
        self.ctx = None
        self.vbo = None
        self.vao = None
        self.grid = None

    @staticmethod
    def make_grid(n=10):
        grid = np.array([], dtype=np.float32)
        for i in range(n * 2 + 1):
            grid = np.append(grid, [i - n, -n])
            grid = np.append(grid, [i - n, n])
            grid = np.append(grid, [-n, i - n])
            grid = np.append(grid, [n, i - n])
        return (grid / n).astype(np.float32)

    def draw_grid(self, color=None, n=10, scale=1.0):
        if self.grid is None:
            self.grid = self.make_grid(n) * scale
        if color is None:
            color = np.tile(np.array([0.5, 0.5, 0.5]),
                            (self.grid.shape[0] // 2, 1))
        grid_buffer = self.ctx.buffer(self.grid.astype("f4"))
        color_buffer = self.ctx.buffer(color.astype("f4"))
        vao_content = [
            (grid_buffer, "2f", 0),
            (color_buffer, "3f /i", 1),
        ]
        vao = self.ctx.vertex_array(self.prog, vao_content)
        vao.render(moderngl.LINES)
        self.release_resources(grid_buffer, color_buffer, vao)

    def draw_particles(self, vertices, indices, point_size=40):
        self.particle_prog["point_size"].value = point_size
        indices_buffer = self.ctx.buffer(np.array(indices, dtype='i4'))
        vertices_buffer = self.ctx.buffer(np.array(vertices, dtype='f4'))

        vao_content = [
            (vertices_buffer, "2f", 0),
            (indices_buffer, "1i", 1),
        ]

        self.vao = self.ctx.vertex_array(self.particle_prog, vao_content)
        self.vao.render(moderngl.POINTS)
        self.release_resources(self.vao, indices_buffer, vertices_buffer)

    def draw_rectangles(self, center: np.ndarray, shape: np.ndarray):
        vert = np.array([], dtype=np.float32)
        n = center.shape[0]
        np.random.seed(1)  # random color
        for i in range(n):
            color = np.random.rand(3)
            # 4 nodes of a rectangle (anti-clockwise)
            nodes = [
                center[i] - shape[i] / 2,
                center[i] + np.array([shape[i, 0], -shape[i, 1]]) / 2,
                center[i] + shape[i] / 2,
                center[i] + np.array([-shape[i, 0], shape[i, 1]]) / 2,
            ]
            indices = np.take(nodes, [0, 1, 3, 1, 2, 3], axis=0)
            for v in indices:
                vert = np.append(vert, v)
                vert = np.append(vert, color)

        # start draw
        self.vbo = self.ctx.buffer(vert.astype(np.float32))
        self.vao = self.ctx.vertex_array(self.prog, self.vbo, "vert",
                                         "vert_color")
        self.vao.render(moderngl.TRIANGLES)

    def draw_polygon(self, vert: np.ndarray, color: np.ndarray):
        vert_buffer = self.ctx.buffer(vert.astype("f4"))
        color_buffer = self.ctx.buffer(color.astype("f4"))
        if vert.shape[0] == color.shape[0]:
            vao_content = [
                (vert_buffer, "2f", "vert"),
                (color_buffer, "3f", "vert_color"),
            ]
        else:
            vao_content = [
                (vert_buffer, "2f", "vert"),
                (color_buffer, "3f /r", "vert_color"),
            ]

        self.vao = self.ctx.vertex_array(self.prog, vao_content)
        self.vao.render(moderngl.LINE_LOOP)
        self.release_resources(self.vao, vert_buffer, color_buffer)

    def draw_circle(self, center: np.ndarray, radius: np.float32,
                    n_div=12, color=np.array([0.0, 0.0, 0.0])):
        angle = np.linspace(0, 2 * np.pi, n_div)
        p = center + radius * np.array([np.cos(angle), np.sin(angle)]).T
        p = np.insert(p, 0, center, axis=0)
        vert = np.hstack((p, np.tile(color, (n_div + 1, 1))))

        self.vbo = self.ctx.buffer(vert.astype(np.float32))
        self.vao = self.ctx.vertex_array(self.prog, self.vbo, "vert",
                                         "vert_color")
        self.vao.render(moderngl.TRIANGLE_FAN)

    def draw_points(self, p: np.ndarray, size=0.1,
                    color=np.array([0.0, 0.0, 0.0])):
        p = p.reshape(-1, 2)
        # color = np.random.random(3) / 8  # random dark color
        for i in range(p.shape[0]):
            self.draw_circle(p[i], radius=size, color=color, n_div=8)

    def draw_connections(self, p: np.ndarray, adj: np.ndarray):
        if adj.shape[0] != p.shape[0]:
            raise ValueError("adj.shape[0] != center.shape[0]")

        n = p.shape[0]
        vert = np.array([], dtype=np.float32)
        color = np.array([0.1, 0.0, 0.1])
        for i in range(n):
            for j in range(i + 1, n):
                if adj[i, j] != 0:
                    vert = np.append(vert, p[i])
                    vert = np.append(vert, color)
                    vert = np.append(vert, p[j])
                    vert = np.append(vert, color)

        # print(vert.shape)
        self.vbo = self.ctx.buffer(vert.astype(np.float32))
        self.vao = self.ctx.vertex_array(self.prog, self.vbo, "vert",
                                         "vert_color")
        self.vao.render(moderngl.LINES)

    def draw_graph(self, nodes, edges):
        # self.draw_connections(nodes, adj)
        vert = np.array([], dtype=np.float32)
        for edge in edges:
            i, j = edge
            vert = np.append(vert, nodes[i])
            vert = np.append(vert, nodes[j])
        self.vbo = self.ctx.buffer(vert.astype(np.float32))
        self.vao = self.ctx.vertex_array(self.prog, self.vbo, "vert")
        self.vao.render(moderngl.LINES)

        self.vao.release()
        self.vbo.release()

        self.draw_particles(
            nodes, np.ones(nodes.shape[0]), point_size=8)

    @staticmethod
    def release_resources(*args):
        for arg in args:
            arg.release()


class Transform2d:
    def __init__(self, scale=[1.0, 1.0], offset=[0., 0.], rotation=0.):
        self.transform = np.eye(3, dtype=np.float32)
        self.scale(*scale)
        self.rotate(rotation)
        self.offset(*offset)

    def set_transform(self, transform):
        self.transform = transform

    @property
    def mat3(self):
        return self.transform.flatten().astype("f4")

    def scale(self, x, y):
        self.transform = np.matmul(self.transform, np.diag([x, y, 1]))

    def rotate(self, theta):
        self.transform = np.matmul(self.transform, np.array([
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta), np.cos(theta), 0],
            [0, 0, 1]
        ]))

    def offset(self, x, y):
        self.transform[2, 0] += x
        self.transform[2, 1] += y
