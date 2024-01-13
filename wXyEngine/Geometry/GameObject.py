class _GameObject:
    GUID = -1

    def __init__(self):
        self.guid = _GameObject.GUID
        _GameObject.GUID += 1

    def update(self, dt):
        pass

    def draw(self):
        pass


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

    @staticmethod
    def reset_global_guid():
        _GameObject.GUID = 0


