import numpy as np
import torch

from wXyEngine import TORCH_DEVICE


class _GameObject:
    __GUID = 0
    device = TORCH_DEVICE

    def __init__(self):
        self.guid = _GameObject.__GUID
        _GameObject.__GUID += 1
        self._lib = torch  # TODO: switch library between torch and numpy

        self.min, self.max = None, None
        self.get_min_max()

    def update(self, dt):
        pass

    def draw(self):
        pass

    def get_min_max(self):  # for AABB
        pass

    def switch_mode(self):
        self._lib = np if self._lib == torch else torch
        print(f"GameObject {self.guid} switched to {self._lib}")

    @staticmethod
    def set_global_torch_device(device):
        _GameObject.device = device


class GameObjectManager:
    def __init__(self):
        self.game_objects = []

    def add(self, game_object):
        self.game_objects.append(game_object)

    def update(self, dt):
        for game_object in self.game_objects:
            game_object.update(dt)

    def draw(self):
        for game_object in self.game_objects:
            game_object.draw()

    def get(self, guid):
        for game_object in self.game_objects:
            if game_object.guid == guid:
                return game_object
        print(f"GameObjectManager.get: guid {guid} not found")
        return None

    def switch_mode(self):  # don't know if this works
        for game_object in self.game_objects:
            game_object.switch_mode()

    @staticmethod
    def reset_global_guid():
        _GameObject.__GUID = 0
