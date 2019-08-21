import json
from .utils import parse_dice_format


class Stat:
    def __init__(self, value=10):
        self._value = value
        self.stat_modifier = 0
        self.temp_stat_modifier = 0

    def randomize(self):
        self._value = parse_dice_format("4d6D1")

    @property
    def value(self):
        return self._value + self.stat_modifier + self.temp_stat_modifier

    @property
    def modifier(self):
        if self.value < 3:
            return -3
        elif 3 <= self.value < 6:
            return -2
        elif 6 <= self.value < 9:
            return -1
        elif 9 <= self.value < 11:
            return 0
        elif 11 <= self.value < 13:
            return 1
        elif 13 <= self.value < 16:
            return 2
        elif 16 <= self.value < 18:
            return 3
        else:
            return 4

    def __ge__(self, other):
        return self.value >= int(other)

    def __le__(self, other):
        return self.value <= int(other)

    def __eq__(self, other):
        return self.value == int(other)

    def __ne__(self, other):
        return self.value != int(other)

    def __lt__(self, other):
        return self.value < int(other)

    def __gt__(self, other):
        return self.value > int(other)

    def __int__(self):
        return int(self.value)

    def recall(self, value):
        self._value = value

    def serialize(self):
        return [self._value, self.modifier]

    def deserialize(self, data):
        self._value, self.stat_modifier = data


class Stats:
    stat_names = ["str", "dex", "int", "chr", "wis", "con"]

    def __init__(self):
        self.str = Stat()
        self.int = Stat()
        self.dex = Stat()
        self.chr = Stat()
        self.con = Stat()
        self.wis = Stat()

    def __getitem__(self, item):
        if not isinstance(item, str):
            raise TypeError

        if item == "str":
            return self.str
        elif item == "int":
            return self.int
        elif item == "dex":
            return self.dex
        elif item == "chr":
            return self.chr
        elif item == "con":
            return self.con
        elif item == "wis":
            return self.wis
        else:
            raise ValueError

    def __str__(self):
        return " ; ".join([f"{stat_name.upper()}: {stat_value}" for stat_name, stat_value in self.as_dict.items()])

    @property
    def as_dict(self):
        return {"str": self.str.value,
                "int": self.int.value,
                "dex": self.dex.value,
                "chr": self.chr.value,
                "con": self.con.value,
                "wis": self.wis.value}

    def recall_stats(self, data):
        for k, v in self.__dict__.items():
            if isinstance(v, Stat):
                v.recall(data[k])

    def randomize(self):
        self.str.randomize()
        self.int.randomize()
        self.dex.randomize()
        self.chr.randomize()
        self.con.randomize()
        self.wis.randomize()

    def serialize(self):
        return {"str": self.str.serialize(),
                "int": self.int.serialize(),
                "dex": self.dex.serialize(),
                "chr": self.chr.serialize(),
                "con": self.con.serialize(),
                "wis": self.wis.serialize()}

    def deserialize(self, data):
        self.str.deserialize(data["str"])
        self.int.deserialize(data["int"])
        self.dex.deserialize(data["dex"])
        self.chr.deserialize(data["chr"])
        self.con.deserialize(data["con"])
        self.wis.deserialize(data["wis"])
        return

    def reset_temp_stats_modifiers(self):
        self.str.temp_stat_modifier = 0
        self.int.temp_stat_modifier = 0
        self.dex.temp_stat_modifier = 0
        self.chr.temp_stat_modifier = 0
        self.con.temp_stat_modifier = 0
        self.wis.temp_stat_modifier = 0


class SavingThrows:
    saving_throws_names = ["poison", "wands", "paralysis", "breath", "spells"]

    def __init__(self, character, data):
        self.character = character
        self._poison = data.get("poison", 10)
        self._wands = data.get("wands", 10)
        self._paralysis = data.get("paralysis", 10)
        self._breath = data.get("breath", 10)
        self._spells = data.get("spells", 10)

    def __getitem__(self, item):
        if not isinstance(item, str):
            raise TypeError

        item = item.lower()
        if item == "poison":
            return self.poison
        elif item == "wands":
            return self.wands
        elif item == "paralysis":
            return self.paralysis
        elif item == "breath":
            return self.breath
        elif item == "spells":
            return self.spells
        else:
            raise ValueError

    @property
    def _level(self):
        return min(self.character.level, 15)

    @property
    def poison(self):
        return self._poison - (self._level // 4) * 2 - self.character.stats.wis.modifier

    @property
    def wands(self):
        return self._wands - (self._level // 4) * 2 - self.character.stats.wis.modifier

    @property
    def paralysis(self):
        return self._paralysis - (self._level // 4) * 2 - self.character.stats.wis.modifier

    @property
    def breath(self):
        return self._breath - (self._level // 4) * 2 - self.character.stats.wis.modifier

    @property
    def spells(self):
        return self._spells - (self._level // 4) * 2 - self.character.stats.wis.modifier


class Job:
    def __init__(self, character, job_name='commoner'):
        self.character = character
        with open("data/jobs.json") as f:
            data = json.load(f)
        self.name = job_name
        self.hp_die = data[job_name]['hp_die']
        self.mp_die = data[job_name]['mp_die']
        self.xp_threshold = data[job_name]['xp_threshold']
        self.saving_throws = SavingThrows(character, data[job_name]["saving_throws"])
        self.primary_stat = data[job_name]["primary_stat"]

    def __str__(self):
        return self.name
