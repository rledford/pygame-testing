from typing import TypedDict

from core.entity import PhysicsEntity


class GameLevelProps(TypedDict):
    tilesize: int
    tiledata: list[int]
    map_w: int
    map_h: int


class GameLevel:
    def __init__(self, props: GameLevelProps):
        self.tilesize = props["tilesize"]
        self.tiledata = props["tiledata"]
        self.map_w = props["map_w"]
        self.map_h = props["map_h"]
        self.start_pos: list[int|float] = [0,0]
        self.platforms: dict[str, PhysicsEntity] = {}
        self.generate_platforms()

    def generate_platforms(self):
        for i, ttype in enumerate(self.tiledata):
            x = int(i % self.map_w)
            y = int(i / self.map_w)
            if ttype == 1:
                self.platforms[f"{x}:{y}"] = PhysicsEntity(
                    {
                        "position": [x * self.tilesize, y * self.tilesize],
                        "bounds": [0, 0, self.tilesize, self.tilesize],
                        "static": True,
                    }
                )
            elif ttype == 2:
                self.start_pos = [x * self.tilesize,y * self.tilesize]
