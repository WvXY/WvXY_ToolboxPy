from time import time

import moderngl
import numpy as np

from PyMRT.Renderer.mdgl_window import Window
from PyMRT.Physics.dynamics import MassSpringSystem

# TODO: integrate this with the Physics module

# ======================================================
n = 20  # number of rooms
dim = 2  # dimension
c = np.random.rand(n, dim) * 10  # center of rooms
# np.random.rand(12)
s = np.random.rand(n, dim) * 8 + 1  # size of rooms
s = np.stack(s, dtype=np.float32)
# c = c - c.mean(axis=0)     # centering
adj = np.ones((n, n))  # graph of rooms
adj = np.triu(adj, 1) + np.tril(adj, -1)


# -----------------visualization------------------------


class GLVisualization(Window):
    gl_version = (3, 3)
    title = "Layout Optimization"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.prog = self.ctx.program(
            vertex_shader="""
                #version 330

                in vec2 vert;
                in vec3 vert_color;

                out vec4 frag_color;

                uniform float scale_global;
                uniform vec2 scale_window;
                // uniform float rotation;

                void main() {
                    frag_color = vec4(vert_color, 0.8);
                    gl_Position = vec4(vert * scale_window / scale_global, 0.0, 1.0);
                }
            """,
            fragment_shader="""
                #version 330
                in vec4 frag_color;
                out vec4 color;
                void main() {
                    color = vec4(frag_color);
                }
            """,
        )
        self.vao, self.vbo = None, None
        self.n, self.dim, self.c, self.s, self.adj = 0, 0, None, None, None

        self.scale_window = self.prog["scale_window"]
        self.scale_global = self.prog["scale_global"]
        # self.color = self.prog['vert_color']
        # self.rotation = self.prog['rotation']
        self.scale_window.value = (0.5, self.aspect_ratio * 0.5)
        self.make_grid()

        self.MSS = None
        self.init_mass_spring_system()

    # -----------------init functions-------------------
    def init_mass_spring_system(self):
        global c, s, adj

        self.n = c.shape[0]
        self.dim = c.shape[1]

        # normalize
        scale = c.max(axis=0) - c.min(axis=0)
        scale = scale.max() * 2
        self.scale_global.value = scale
        offset = (c.max(axis=0) + c.min(axis=0)) / 2

        self.c = c - offset
        self.s = s
        self.adj = adj
        self.MSS = MassSpringSystem(self.c, self.s, self.adj, lr=1e-6, beta=0.9)
        # momentum term: lr = 3e-4, beta = 0.9

    def make_grid(self, n=60):
        """
        make a grid with n*2+1 lines
        n: half of the number of lines
        """
        self.grid = np.array([], dtype=np.float32)
        color = np.array([0.8, 0.8, 0.8])
        for i in range(n * 2 + 1):
            self.grid = np.append(self.grid, [i - n, -n])
            self.grid = np.append(self.grid, color)
            self.grid = np.append(self.grid, [i - n, n])
            self.grid = np.append(self.grid, color)
            self.grid = np.append(self.grid, [-n, i - n])
            self.grid = np.append(self.grid, color)
            self.grid = np.append(self.grid, [n, i - n])
            self.grid = np.append(self.grid, color)
        self.grid = self.grid.astype(np.float32)

    # -----------------draw functions-------------------

    def draw_grid(self):
        self.vbo = self.ctx.buffer(self.grid.tobytes())
        self.vao = self.ctx.simple_vertex_array(
            self.prog, self.vbo, "vert", "vert_color"
        )
        self.vao.render(moderngl.LINES)

    def draw_rectangles(self):
        vert = np.array([], dtype=np.float32)
        np.random.seed(1)  # for color
        for i in range(self.n):
            icolor = np.random.rand(3)
            # 4 nodes of a rectangle (anti-clockwise)
            nodes = [
                self.c[i] - self.s[i] / 2,
                self.c[i] + np.array([self.s[i, 0], -self.s[i, 1]]) / 2,
                self.c[i] + self.s[i] / 2,
                self.c[i] + np.array([-self.s[i, 0], self.s[i, 1]]) / 2,
            ]
            indicies = np.take(nodes, [0, 1, 3, 1, 2, 3], axis=0)
            for v in indicies:
                vert = np.append(vert, v)
                vert = np.append(vert, icolor)

        # start draw
        self.vbo = self.ctx.buffer(vert.astype(np.float32))
        self.vao = self.ctx.vertex_array(self.prog, self.vbo, "vert", "vert_color")
        self.vao.render(moderngl.TRIANGLES)

    def draw_connections(self):
        vert = np.array([])
        color = np.array([0.1, 0.0, 0.1])
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.MSS.adj[i, j] != 0:
                    vert = np.append(vert, self.c[i])
                    vert = np.append(vert, color)
                    vert = np.append(vert, self.c[j])
                    vert = np.append(vert, color)

        # print(vert.shape)
        self.vbo = self.ctx.buffer(np.array(vert, dtype="f4"))
        self.vao = self.ctx.vertex_array(self.prog, self.vbo, "vert", "vert_color")
        self.vao.render(moderngl.LINES)

    def draw_circle(
            self,
            center: np.ndarray,
            radius: np.float32,
            n=64,
            color=np.array([0.0, 0.0, 0.0]),
    ):
        angle = np.linspace(0, 2 * np.pi, n)
        p = center + radius * np.array([np.cos(angle), np.sin(angle)]).T
        p = np.insert(p, 0, center, axis=0)
        vert = np.hstack((p, np.tile(color, (n + 1, 1))))

        self.vbo = self.ctx.buffer(vert.astype(np.float32))
        self.vao = self.ctx.vertex_array(self.prog, self.vbo, "vert", "vert_color")
        self.vao.render(moderngl.TRIANGLE_FAN)

    def draw_points(self, p: np.ndarray, size=0.1):
        n = p.shape[0]
        vert = np.array([])
        color = np.random.random(3) / 8  # random dark color
        for i in range(n):
            self.draw_circle(p[i], size, color=color, n=16)

    # ----------------------render------------------------

    def render(self, time: float, frame_time: float):
        # clean
        self.ctx.clear(1.0, 1.0, 1.0)
        self.ctx.enable(moderngl.BLEND)

        if self.wnd.is_key_pressed(122):  # z
            self.MSS.optimize()

        self.draw_grid()
        self.draw_rectangles()
        self.draw_connections()
        self.draw_points(self.MSS.c, size=0.5)


if __name__ == "__main__":
    # np.random.seed(0)
    GLVisualization.run()
