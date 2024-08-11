from pathlib import Path

import moderngl
import numpy as np

from .mdgl_window import Window
from .voronoi_system import VoronoiPushData, VoronoiSystem


# some drawing functions
class Renderer2D(Window):
    """
    This is a 2D renderer based on ModernGL.
    Draw functions are implemented here.
    """

    title = "ModernGL 2D Renderer"
    resource_dir = Path(__file__).parent.resolve()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prog = self.load_program("shaders/basic_shader.glsl")
        self.particle_prog = self.load_program("shaders/particle.glsl")
        # self.voronoi_prog = self.load_program("shaders/voronoi.glsl")

        self.voronoi_system = VoronoiSystem(ctx=self.ctx)

        self.grid = None

    def render(self, time: float, frame_time: float):
        self.ctx.clear(1.0, 1.0, 1.0)
        self.ctx.enable(moderngl.BLEND)

    def map_wnd_to_gl(self, x, y):
        return x / self.wnd.width * 2 - 1, 1 - y / self.wnd.height * 2

    @staticmethod
    def release_resources(*args):
        for arg in args:
            arg.release()

    @staticmethod
    def make_grid(n=10):  # deprecate this
        grid = np.array([], dtype="f4")
        for i in range(n * 2 + 1):
            grid = np.append(grid, [i - n, -n])
            grid = np.append(grid, [i - n, n])
            grid = np.append(grid, [-n, i - n])
            grid = np.append(grid, [n, i - n])
        return (grid / n).astype("f4")

    # some drawing functions
    def draw_grid(self, color=None, n=10, scale=1.0):
        if self.grid is None:  # TODO: fix this
            self.grid = self.make_grid(n) * scale
        if color is None:
            color = np.tile(
                np.array([0.5, 0.5, 0.5]), (self.grid.shape[0] // 2, 1)
            )
        grid_buffer = self.ctx.buffer(self.grid.astype("f4"))
        color_buffer = self.ctx.buffer(color.astype("f4"))
        vao_content = [
            (grid_buffer, "2f", 0),
            (color_buffer, "3f /i", 1),
        ]
        vao = self.ctx.vertex_array(self.prog, vao_content)
        vao.render(moderngl.LINES)
        self.release_resources(grid_buffer, color_buffer, vao)

    def draw_particles(
        self, vertices: np.ndarray, indices=None, point_size=40, use_circle=True
    ):
        self.particle_prog["point_size"].value = point_size
        self.particle_prog["use_circle"].value = use_circle
        vertices_buffer = self.ctx.buffer(np.array(vertices, dtype="f4"))

        has_indices = indices is not None
        if has_indices:
            indices_buffer = self.ctx.buffer(np.array(indices, dtype="i4"))
            vao_content = [
                (vertices_buffer, "2f", 0),
                (indices_buffer, "1i", 1),
            ]
        else:
            vao_content = [
                (vertices_buffer, "2f", 0),
                # (indices_buffer, "1i /r", 1), # maybe specify a color
            ]

        vao = self.ctx.vertex_array(self.particle_prog, vao_content)
        vao.render(moderngl.POINTS)

        if has_indices:
            self.release_resources(vao, vertices_buffer, indices_buffer)
        else:
            self.release_resources(vao, vertices_buffer)

    def draw_rectangles(
        self, center: np.ndarray, shape: np.ndarray
    ):  # TODO: optimize this
        vert = np.array([], dtype="f4")
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
        vbo = self.ctx.buffer(vert.astype("f4"))
        vao = self.ctx.vertex_array(self.prog, vbo, "vert", "vert_color")
        vao.render(moderngl.TRIANGLES)
        self.release_resources(vao, vbo)

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

    def draw_circle(
        self,
        center: np.ndarray,
        radius: float,
        n_div=12,
        color=np.array([0.0, 0.0, 0.0]),
    ):
        angle = np.linspace(0, 2 * np.pi, n_div)
        p = center + radius * np.array([np.cos(angle), np.sin(angle)]).T
        p = np.insert(p, 0, center, axis=0)
        vert = np.hstack((p, np.tile(color, (n_div + 1, 1))))

        self.vbo = self.ctx.buffer(vert.astype("f4"))
        self.vao = self.ctx.vertex_array(
            self.prog, self.vbo, "vert", "vert_color"
        )
        self.vao.render(moderngl.TRIANGLE_FAN)

    def draw_connections(self, p: np.ndarray, adj: np.ndarray):
        if adj.shape[0] != p.shape[0]:
            raise ValueError("adj.shape[0] != center.shape[0]")

        n = p.shape[0]
        vert = np.array([], dtype="f4")
        color = np.array([0.1, 0.0, 0.1])
        for i in range(n):
            for j in range(i + 1, n):
                if adj[i, j] != 0:
                    vert = np.append(vert, p[i])
                    vert = np.append(vert, color)
                    vert = np.append(vert, p[j])
                    vert = np.append(vert, color)

        # print(vert.shape)
        self.vbo = self.ctx.buffer(vert.astype("f4"))
        self.vao = self.ctx.vertex_array(
            self.prog, self.vbo, "vert", "vert_color"
        )
        self.vao.render(moderngl.LINES)

    def draw_graph(self, vertices, edges):  # TODO: optimize this
        vert = np.array([], dtype="f4")
        for edge in edges:
            i, j = edge
            vert = np.append(vert, vertices[i])
            vert = np.append(vert, vertices[j])
        vbo = self.ctx.buffer(vert.astype("f4"))
        vao = self.ctx.vertex_array(self.prog, vbo, "vert")
        vao.render(moderngl.LINES)

        self.release_resources(vao, vbo)

        self.draw_particles(vertices, np.ones(vertices.shape[0]), point_size=8)

