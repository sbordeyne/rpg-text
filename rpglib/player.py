import json


class Job:
    def __init__(self, job_name='commoner'):
        with open("data/jobs.json") as f:
            data = json.load(f)
        self.name = job_name
        self.hp_multiplier = data[job_name]['hp_multiplier']
        self.mp_multiplier = data[job_name]['mp_multiplier']
        self.xp_threshold = data[job_name]['xp_threshold']

    def __str__(self):
        return self.name


class Item:
    def __init__(self, name):
        self.name = name
        with open("data/items.json") as f:
            self.set_attributes(json.load(f))

    def set_attributes(self, obj):
        pass


class Inventory:
    def __init__(self):
        self.items = []
        self.money = 0

    def get_item(self, item):
        if isinstance(item, str):
            item = Item(item)
        self.items.append(item)

    def serialize(self):
        return {"items": self.items,
                "money": self.money}

    def deserialize(self, data):
        self.items = data["items"]
        self.money = data["money"]


class Player:
    def __init__(self, game, name, job_name='commoner"'):
        self.game = game
        self.name = name
        self.job = Job(job_name)
        self.experience = 0
        self._health = self.max_health
        self._mana = self.max_mana
        self.status_effects = []
        self.location = self.game.map.get_location_from_position((0, 0))
        self.inventory = Inventory()

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, amount):
        self._health = amount

    @property
    def max_health(self):
        return self.level * self.job.hp_multiplier

    @property
    def mana(self):
        return self._mana

    @mana.setter
    def mana(self, amount):
        self._mana = amount

    @property
    def max_mana(self):
        return self.level * self.job.mp_multiplier

    @property
    def level(self):
        THRESHOLD = self.job.xp_threshold  # XP points to first level
        i = 1
        current_threshold = THRESHOLD
        while self.experience > current_threshold:
            i += 1
            current_threshold += THRESHOLD * i
        return i

    @property
    def position(self):
        return self.location.position

    def __str__(self):
        return \
            f"""Player {self.name} ; {self.health}/{self.max_health} HP ; {self.mana}/{self.max_mana} MP
Location : {str(self.location)} ; Level {self.level} {str(self.job).capitalize()}"""

    def move(self, direction):
        """Moves the player in $direction (n, s, w, e)"""
        location = self.location.try_move_to(direction)
        if location is not None:
            self.location = location

    def serialize(self):
        data = {"job": self.job.name,
                "experience": self.experience,
                "health": self._health,
                "mana": self._mana,
                "position": self.position.tuple,
                "status_effects": self.status_effects,
                "inventory": self.inventory.serialize()
                }
        return data

    def deserialize(self, data):
        self.job = Job(data["job"])
        self.experience = data["experience"]
        self._health = data["health"]
        self._mana = data["mana"]
        self.location = self.game.map.get_location_from_position(data["position"])
        self.status_effects = data["status_effects"]
        self.inventory.deserialize(data["inventory"])
        return
