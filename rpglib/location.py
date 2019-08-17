from .utils import Vector2, display


class Location:
    def __init__(self, world_map, data):
        self.x = data["position"][0]
        self.y = data["position"][1]
        self.name = data["name"]

        self.exits = data.get("exits", ['n', 's', 'w', 'e'])
        self.map_icon = data.get("map_icon", '-')
        self.npc = data.get("npc", [])
        self.map = world_map

    @property
    def position(self):
        return Vector2(self.x, self.y)

    def try_move_to(self, direction):
        direction = direction[0].lower()
        if direction in self.exits:
            return self.map.get_location_from_position(self.position)
        else:
            display("Can't go there!")

    def __str__(self):
        return f"{self.name} ({self.x}, {self.y})"

    def info(self):
        return f"{str(self)} ; Exits : {self.exits} ; NPCs : {self.npc}"

    def serialize(self):
        return {}

    def deserialize(self, data):
        return