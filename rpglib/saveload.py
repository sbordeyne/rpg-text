import json
import glob
import os


class SaveSystem:
    def __init__(self, game):
        self.game = game

    def save(self, save_name):
        if save_name == "list":
            print("Save name 'list' is reserved, please choose a different save name.")
            return

        if not os.path.exists("saves"):
            os.mkdir("saves")

        data = {"game": self.game.serialize(),
                "player": self.game.player.serialize(),
                "map": self.game.map.serialize(),
                "characters": self.game.character_system.serialize()}
        with open(f"saves/{save_name}.json", "w") as save_file:
            json.dump(data, save_file)
        pass

    def load(self, save_name):
        pass

    @staticmethod
    def get_save_names(self):
        if not os.path.exists("saves"):
            return []
        
        return [name.split(".")[0] for name in glob.glob("saves/*.json")]
