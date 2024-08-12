import moderngl
import numpy as np

from .system_base import SystemBase


# TODO: refactor the draw functions
class BasicSystem(SystemBase):
    def __init__(self, ctx):
        super().__init__(ctx, "./shaders/basic_shader.glsl")
        self.vao, self.vbo, self.ebo = None, None, None

    def create_buffer(self, vertices: np.ndarray, indices=None, color=None):
        if color is None:
            color = np.ones(vertices.shape[0])
        if indices is None:
            indices = np.arange(vertices.shape[0])

        vert = np.hstack((vertices, color))
        vert = vert.flatten()

        self.vbo = self.ctx.buffer(vert.astype("f4"))
        self.ebo = self.ctx.buffer(indices.astype("i4"))

    def setup(self):
        self.vao = self.ctx.vertex_array(
            self._program,
            [(self.vbo, "2f 3f", "vert"), (self.ebo, "i4", "indices")],
        )

    def draw(self, mode=moderngl.TRIANGLES):
        self.setup()
        self.vao.render(mode)
        self._release(self.vao, self.vbo, self.ebo)

    def draw_grid(self, grid, color=None):
        if color is None:
            color = np.tile(np.array([0.5, 0.5, 0.5]), (grid.shape[0] // 2, 1))
        grid_buffer = self.ctx.buffer(grid.astype("f4"))
        color_buffer = self.ctx.buffer(color.astype("f4"))
        vao_content = [
            (grid_buffer, "2f", 0),
            (color_buffer, "3f /i", 1),
        ]
        vao = self.ctx.vertex_array(self._program, vao_content)
        vao.render(moderngl.LINES)
        self._release(grid_buffer, color_buffer, vao)

    # def draw_particles(
    #         self, vertices: np.ndarray, indices=None, point_size=40, use_circle=True
    # ):

    # def draw_rectangles(
    #         self, center: np.ndarray, shape: np.ndarray
    # ):  # TODO: optimize this
    #     vert = np.array([], dtype="f4")
    #     n = center.shape[0]
    #     np.random.seed(1)  # random color
    #     for i in range(n):
    #         color = np.random.rand(3)
    #         # 4 nodes of a rectangle (anti-clockwise)
    #         nodes = [
    #             center[i] - shape[i] / 2,
    #             center[i] + np.array([shape[i, 0], -shape[i, 1]]) / 2,
    #             center[i] + shape[i] / 2,
    #             center[i] + np.array([-shape[i, 0], shape[i, 1]]) / 2,
    #             ]
    #         indices = np.take(nodes, [0, 1, 3, 1, 2, 3], axis=0)
    #         for v in indices:
    #             vert = np.append(vert, v)
    #             vert = np.append(vert, color)
    #
    #     # start draw
    #     vbo = self.ctx.buffer(vert.astype("f4"))
    #     vao = self.ctx.vertex_array(self._program, vbo, "vert", "vert_color")
    #     vao.render(moderngl.TRIANGLES)
    #     self.release_resources(vao, vbo)

    # def draw_polygon(self, vert: np.ndarray, color: np.ndarray):
    #     vert_buffer = self.ctx.buffer(vert.astype("f4"))
    #     color_buffer = self.ctx.buffer(color.astype("f4"))
    #     if vert.shape[0] == color.shape[0]:
    #         vao_content = [
    #             (vert_buffer, "2f", "vert"),
    #             (color_buffer, "3f", "vert_color"),
    #         ]
    #     else:
    #         vao_content = [
    #             (vert_buffer, "2f", "vert"),
    #             (color_buffer, "3f /r", "vert_color"),
    #         ]
    #
    #     self.vao = self.ctx.vertex_array(self._program, vao_content)
    #     self.vao.render(moderngl.LINE_LOOP)
    #     self._release(self.vao, vert_buffer, color_buffer)
    #
    # def draw_circle(
    #     self,
    #     center: np.ndarray,
    #     radius: float,
    #     n_div=12,
    #     color=np.array([0.0, 0.0, 0.0]),
    # ):
    #     angle = np.linspace(0, 2 * np.pi, n_div)
    #     p = center + radius * np.array([np.cos(angle), np.sin(angle)]).T
    #     p = np.insert(p, 0, center, axis=0)
    #     vert = np.hstack((p, np.tile(color, (n_div + 1, 1))))
    #
    #     self.vbo = self.ctx.buffer(vert.astype("f4"))
    #     self.vao = self.ctx.vertex_array(
    #         self._program, self.vbo, "vert", "vert_color"
    #     )
    #     self.vao.render(moderngl.TRIANGLE_FAN)
    #
    # def draw_connections(self, p: np.ndarray, adj: np.ndarray):
    #     if adj.shape[0] != p.shape[0]:
    #         raise ValueError("adj.shape[0] != center.shape[0]")
    #
    #     n = p.shape[0]
    #     vert = np.array([], dtype="f4")
    #     color = np.array([0.1, 0.0, 0.1])
    #     for i in range(n):
    #         for j in range(i + 1, n):
    #             if adj[i, j] != 0:
    #                 vert = np.append(vert, p[i])
    #                 vert = np.append(vert, color)
    #                 vert = np.append(vert, p[j])
    #                 vert = np.append(vert, color)
    #
    #     # print(vert.shape)
    #     self.vbo = self.ctx.buffer(vert.astype("f4"))
    #     self.vao = self.ctx.vertex_array(
    #         self._program, self.vbo, "vert", "vert_color"
    #     )
    #     self.vao.render(moderngl.LINES)
    #
    # def draw_graph(self, vertices, edges):  # TODO: optimize this
    #     vert = np.array([], dtype="f4")
    #     for edge in edges:
    #         i, j = edge
    #         vert = np.append(vert, vertices[i])
    #         vert = np.append(vert, vertices[j])
    #     vbo = self.ctx.buffer(vert.astype("f4"))
    #     vao = self.ctx.vertex_array(self._program, vbo, "vert")
    #     vao.render(moderngl.LINES)
    #
    #     self._release(vao, vbo)

    # self.draw_particles(vertices, np.ones(vertices.shape[0]), point_size=8)
