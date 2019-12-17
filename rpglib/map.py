from .location import Location
import json
from .utils import Vector2, clear_screen
import sys


class Map:
    def __init__(self, game):
        self.locations = []
        with open("data/map.json") as f:
            data = json.load(f)
        for location in data:
            self.locations.append(Location(self, location))
        self.game = game

    def get_location_from_position(self, position):
        """If position refers to a valid location on the map,
        return that location. Otherwise, return None"""
        position = Vector2(position)
        for location in self.locations:
            if location.position == position:
                return location
        return None

    def remove_opponent(self, opponent):
        loc = self.game.player.location
        loc.remove_opponent(opponent)

    def display(self, radius=1):
        """Shows the map."""
        clear_screen()
        offsets = [[(x, y) for x in range(-radius, radius + 1)] for y in range(-radius, radius + 1)]

        for row in offsets:
            for offset in row:
                loc = self.get_location_from_position(self.game.player.position + Vector2(*offset))
                if loc is not None:
                    sys.stdout.write(loc.map_icon)
                else:
                    sys.stdout.write(" ")
            sys.stdout.write("\n")

    def serialize(self):
        data = [location.serialize() for location in self.locations]
        return data

    def deserialize(self, data):
        for location, loc_data in zip(self.locations, data):
            location.deserialize(loc_data)
        return
