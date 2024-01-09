from time import time

import moderngl
import moderngl_window as mglw
import numpy as np
from pyrr import Matrix44


class Window(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "Research 3D Visualization"
    window_size = (1280, 720)
    aspect_ratio = 16 / 9
    resizable = True
    samples = 4  # anti-aliasing
    cursor = True
    point_size = 100
    vsync = False


# ======================================================
# -----------------visualization------------------------
class MGL3(Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.prog = self.ctx.program(
            vertex_shader="""
                #version 330
                
                // uniform float scale_global;
                // uniform vec2 scale_window;
                uniform mat4 Mvp;
                
                in vec3 vert;
                in vec3 vert_color;
                
                out vec4 frag_color;
                out vec3 frag_vert;

                void main() 
                {
                    frag_color = vec4(vert_color, 1.);
                    gl_Position = Mvp * vec4(vert, 1.0);
                    frag_vert = vert;
                }
            """,
            fragment_shader="""
                #version 330
                
                uniform vec3 Light;
                
                in vec3 frag_vert;
                in vec4 frag_color;
                
                out vec4 color;
                
                void main() 
                {
                    float lum = clamp(dot(normalize(Light - frag_vert), 
                        normalize(frag_color.xyz)), 0.0, 1.0)* 0.8 + 0.2;
                    color = vec4(frag_color.xyz * lum, 1.0);
                }
            """,
        )

        self.mvp = self.prog["Mvp"]
        self.light = self.prog["Light"]
        self.light.value = (1, 1, 1)
        self.make_grid()

    def make_grid(self, n=60):
        """
        make a grid with n*2+1 lines
        n: half of the number of lines
        """
        grid = []
        color = np.array([0.5, 0.5, 0.5])
        for i in range(n * 2 + 1):
            g_color = color
            if i == n:
                g_color = np.array([1.0, 0.0, 0.0])
            grid.append([[i - n, -n, 0], g_color])
            grid.append([[i - n, n, 0], g_color])
            grid.append([[-n, i - n, 0], g_color])
            grid.append([[n, i - n, 0], g_color])
        self.grid = np.ravel(grid).astype("f4")

    def draw_grid(self):
        vbo = self.ctx.buffer(self.grid)
        vao = self.ctx.vertex_array(self.prog, vbo, "vert", "vert_color")
        vao.render(moderngl.LINES)

    def draw_rectangles(self, center: np.ndarray, shape: np.ndarray):
        if center.shape[0] != shape.shape[0]:
            raise ValueError("center.shape[0] != shape.shape[0]")

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
        vbo = self.ctx.buffer(vert.astype(np.float32))
        vao = self.ctx.vertex_array(self.prog, vbo, "vert", "vert_color")
        vao.render(moderngl.TRIANGLES)

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

        vbo = self.ctx.buffer(vert.astype(np.float32))
        vao = self.ctx.vertex_array(self.prog, vbo, "vert", "vert_color")
        vao.render(moderngl.TRIANGLE_FAN)

    def draw_points(self, p: np.ndarray, size=0.1):
        n = p.shape[0]
        vert = np.array([])
        color = np.random.random(3) / 8  # random dark color
        for i in range(n):
            self.draw_circle(p[i], size, color=color, n=16)

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
        vbo = self.ctx.buffer(vert.astype(np.float32))
        vao = self.ctx.vertex_array(self.prog, vbo, "vert", "vert_color")
        vao.render(moderngl.LINES)

    def set_mvp(self, camera_pos, angle):
        # camera_pos = (np.cos(angle) * 3.0, np.sin(angle) * 3.0, 2.0)

        proj = Matrix44.perspective_projection(80.0, self.aspect_ratio, 0.1, 100.0)
        lookat = Matrix44.look_at(
            camera_pos,
            (0.0, 0.0, 0.5),
            (0.0, 0.0, 5.0),
        )
        self.mvp.write((proj * lookat).astype("f4").tobytes())
        self.light.value = camera_pos

    # texture
    # def draw_picture(self):
    #     width, height = self.window_size
    #
    #     # pixels = os.urandom(width * height * 4)
    #     # pixels = np.random.rand(width * height * 4).tobytes()
    #     pixels = np.random.random(width * height * 4).astype('f4').tobytes()
    #     # pixels = np.random.random(width * height * 4).tobytes()
    #     texture = ctypes.c_uint32()
    #     GL.glGenTextures(1, ctypes.byref(texture))
    #     GL.glActiveTexture(GL.GL_TEXTURE0)
    #     GL.glBindTexture(GL.GL_TEXTURE_2D, texture)
    #     GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA8, width, height, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, pixels)
    #     GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST)
    #     GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST)
    #     self.texture = self.ctx.external_texture(texture.value, (width, height), 4, 0, 'f1')

    # ---------------------------------------------
    # ---------------render loop-------------------
    def render(self, time, frame_time):
        # clear screen
        self.ctx.clear(0.1, 0.1, 0.1)
        self.ctx.enable(moderngl.DEPTH_TEST)

        # ==================

        angle = time * 0.2
        camera_pos = (np.cos(angle) * 3.0, np.sin(angle) * 3.0, 2.0)
        self.set_mvp(camera_pos, angle)
        # self.light.value = camera_pos

        self.draw_grid()
        # ==================
        self.draw_rectangles(np.array([[0, 0]]), np.array([[1, 1]]))

        # vao.render()
