import json


class Character:
    def __init__(self, name, data=None):
        if data is None:
            data = {}
        self.name = name
        self.description = data.get("description", "")
        pass

    def start_dialogue(self):
        pass

    def info(self):
        return f'{self.name} : {self.description}'


class CharacterSystem:
    def __init__(self, game):
        self.game = game
        with open("data/characters.json") as f:
            data = json.load(f)
        self.characters = {k: Character(k, v) for k, v in data.items()}

    def talk(self, recipient):
        """Talk to character $character_name"""
        self.characters.get(recipient).start_dialogue()

    def info(self):
        return "\n".join([self.characters.get(char_name, Character(char_name)).info()
                          for char_name in self.game.player.location.npc])

    def serialize(self):
        return {}

    def deserialize(self, data):
        return