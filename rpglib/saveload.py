import json
import glob
import os
import datetime


class SaveSystem:
    def __init__(self, game):
        self.game = game

    def save(self, save_name):
        """Saves the current game with name $save_name"""
        if save_name == "list":
            print("Save name 'list' is reserved, please choose a different save name.")
            return

        if not os.path.exists("saves"):
            os.mkdir("saves")

        data = {"timestamp": str(datetime.datetime.now().timestamp()),
                "timer": self.game.timer.serialize(),
                "player": self.game.player.serialize(),
                "map": self.game.map.serialize(),
                "characters": self.game.character_system.serialize()}
        with open(f"saves/{save_name}.json", "w") as save_file:
            json.dump(data, save_file, indent=4)
        pass

    def load(self, save_name):
        """Loads saved game named $save_name"""
        if not os.path.exists("saves"):
            print("No saves found.")
            return

        with open(f"saves/{save_name}.json", "w") as save_file:
            data = json.load(save_file)
        self.game.timer.deserialize(data["timer"])
        self.game.player.deserialize(data["player"])
        self.game.map.deserialize(data["map"])
        self.game.character_system.deserialize(data["characters"])
        pass

    @staticmethod
    def get_save_names(self):
        if not os.path.exists("saves"):
            return []

        return [name.split(".")[0] for name in glob.glob("saves/*.json")]
