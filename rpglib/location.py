from .utils import Vector2, display


class Location:
    def __init__(self, world_map, data):
        self.x = data["position"][0]
        self.y = data["position"][1]
        self.name = data["name"]

        self.exits = data.get("exits", [])
        self.map_icon = data.get("map_icon", '-')
        self.description = "\n".join([f"Entered {str(self)}",
                                      data.get("description", "")])
        self.npc = data.get("npc", [])
        self.map = world_map

    @property
    def position(self):
        return Vector2(self.x, self.y)

    def try_move_to(self, direction):
        direction = direction[0].lower()
        if direction in self.exits:
            vectors = {"n": Vector2(0, -1),
                       "e": Vector2(1, 0),
                       "s": Vector2(0, 1),
                       "w": Vector2(-1, 0)}
            new_position = self.position + vectors[direction]
            return self.map.get_location_from_position(new_position)
        else:
            display("Can't go there!")

    def __str__(self):
        return f"{self.name} ({self.x}, {self.y})"

    def info(self):
        return f"{str(self)} ; Exits : {self.exits} ; NPCs : {self.npc}"

    def remove_opponent(self, opponent):
        return

    def serialize(self):
        return {}

    def deserialize(self, data):
        return