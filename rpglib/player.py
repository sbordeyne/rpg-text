import json
from .inventory_system import Inventory
from .entity import Entity


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


class Player(Entity):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.name = None
        self._job = None
        self.experience = 0
        self._health = self.max_health
        self._mana = self.max_mana
        self.location = self.game.map.get_location_from_position((0, 0))
        self.inventory = Inventory()
        self.damage = ("hands", 0, None)

    @property
    def job(self):
        return self._job

    @job.setter
    def job(self, value):
        if isinstance(value, str):
            self._job = Job(value)
        elif isinstance(value, Job):
            self._job = value
        else:
            raise ValueError

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

    @property
    def ac(self):
        return 9 - self.inventory.equipped.get_total_ac()

    @property
    def ac_modifier(self):
        return self.stats.dex.modifier

    @property
    def hit_modifier(self):
        return max(self.stats.dex.modifier, self.stats.str.modifier)

    def __str__(self):
        return \
            f"""Player {self.name} ; {self.health}/{self.max_health} HP ; {self.mana}/{self.max_mana} MP
Location : {str(self.location)} ; Level {self.level} {str(self.job).capitalize()}"""

    def move(self, direction):
        """Moves the player in $direction (n, s, w, e)"""
        location = self.location.try_move_to(direction)
        if location is not None:
            self.location = location

    def gain_experience(self, xp_value):
        self.experience += xp_value
        for effect in self.status_effects:
            effect.remove()
        self.status_effects = []
        self.stats.reset_temp_stats_modifiers()

    def serialize(self):
        data = {"job": self.job.name,
                "experience": self.experience,
                "health": self._health,
                "mana": self._mana,
                "position": self.position.tuple,
                "status_effects": self.status_effects,
                "inventory": self.inventory.serialize(),
                "stats": self.stats.serialize(),
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
        self.stats.deserialize(data["stats"])
        return
