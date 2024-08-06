import numpy as np


class VoronoiPushData:
    __MAX_SEEDS = 128

    def __init__(self, seeds=None):
        self.seeds = np.empty([self.__MAX_SEEDS, 3], dtype="f4")
        if seeds is not None:
            self.len = len(seeds)
            self.seeds[: self.len] = seeds
        else:
            self.len = 0

    def update(self, seeds):
        self.seeds.fill(0)
        self.len = len(seeds)
        self.seeds[: self.len] = seeds

    def tobytes(self):
        return self.seeds.tobytes() + self.len.to_bytes(4, "little")
