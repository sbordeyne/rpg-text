from .location import Location
import json
from .utils import Vector2, clear_screen
import sys


class Map:
    locations = []

    def __init__(self, game):
        with open("data/map.json") as f:
            data = json.load(f)
        for location in data:
            self.locations.append(Location(self, location))
        self.game = game

    def get_location_from_position(self, position):
        position = Vector2(position)
        for location in self.locations:
            if location.position == position:
                return location
        return self.locations[0]

    def display(self):
        """Shows the map."""
        loc00 = self.get_location_from_position(self.game.player.position + Vector2(-1, -1))
        loc10 = self.get_location_from_position(self.game.player.position + Vector2(0, -1))
        loc20 = self.get_location_from_position(self.game.player.position + Vector2(1, -1))
        loc01 = self.get_location_from_position(self.game.player.position + Vector2(-1, 0))
        loc11 = self.game.player.location
        loc21 = self.get_location_from_position(self.game.player.position + Vector2(1, 0))
        loc02 = self.get_location_from_position(self.game.player.position + Vector2(-1, 1))
        loc12 = self.get_location_from_position(self.game.player.position + Vector2(0, 1))
        loc22 = self.get_location_from_position(self.game.player.position + Vector2(1, 1))
        clear_screen()
        sys.stdout.write(loc00.map_icon)
        sys.stdout.write(loc10.map_icon)
        sys.stdout.write(loc20.map_icon)
        sys.stdout.write("\n")
        sys.stdout.write(loc01.map_icon)
        sys.stdout.write(loc11.map_icon)
        sys.stdout.write(loc21.map_icon)
        sys.stdout.write("\n")
        sys.stdout.write(loc02.map_icon)
        sys.stdout.write(loc12.map_icon)
        sys.stdout.write(loc22.map_icon)
        sys.stdout.write("\n")
