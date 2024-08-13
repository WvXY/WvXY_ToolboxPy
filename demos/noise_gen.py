import numpy as np
import torch
import moderngl

from pymrt.Interface.interface import SimpleApp

WIDTH, HEIGHT = 100, 100
from pymrt import TORCH_DEVICE


def generate_noise(width, height):
    return torch.rand((width, height), device=TORCH_DEVICE)
    # return np.random.rand(width, height)
    # return np.random.randint(0, 2, (width, height))  # binary noise


def median_filter(noise):
    for i in range(1, noise.shape[0] - 1):
        for j in range(1, noise.shape[1] - 1):
            filter33 = noise[i - 1 : i + 2, j - 1 : j + 2]
            # noise[i, j] = np.mean(filter33)
            noise[i, j] = torch.median(filter33)


def normalize(noise):
    return (noise - noise.min()) / (noise.max() - noise.min())


class NoiseApp(SimpleApp):
    window_size = (WIDTH * 3, HEIGHT * 3)
    aspect_ratio = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.noise = generate_noise(WIDTH, HEIGHT)

    def render(self, time, frame_time):
        self.ctx.clear(0.0, 0.0, 0.0)
        self.ctx.enable(moderngl.BLEND)  # | moderngl.DEPTH_TEST

        median_filter(self.noise)
        data = np.array([self.noise.cpu().numpy() * 255] * 3, dtype=np.uint8).T

        self.image_system.create_buffer(data)
        self.image_system.draw()


if __name__ == "__main__":
    NoiseApp.run()
