import json
import random
from .utils import MaxLenList


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


class EquipmentInventory:
    def __init__(self, inventory):
        self.inventory = inventory
        self.head = None
        self.body = None
        self.legs = None
        self.r_hand = None
        self.l_hand = None
        self.rings = MaxLenList(maxlen=2)

    def equip(self, item):
        if item.slot == "head":
            self.de_equip("head")
            self.head = item
        elif item.slot == "body":
            self.de_equip("body")
            self.body = item
        elif item.slot == "legs":
            self.de_equip("legs")
            self.legs = item
        elif item.slot == "r_hand":
            self.de_equip("r_hand")
            self.r_hand = item
        elif item.slot == "l_hand":
            self.de_equip("l_hand")
            self.l_hand = item
        elif item.slot == "rings":
            popped_out = self.rings.append(item)
            self.inventory.get_item(popped_out)
        self.inventory.remove_item(item)

    def de_equip(self, slot):
        """De-equips item in $slot. $slot can be 'all' to de-equip everything"""
        if slot == "head":
            self.inventory.get_item(self.head)
            self.head = None
        elif slot == "body":
            self.inventory.get_item(self.body)
            self.body = None
        elif slot == "legs":
            self.inventory.get_item(self.legs)
            self.legs = None
        elif slot == "r_hand":
            self.inventory.get_item(self.r_hand)
            self.r_hand = None
        elif slot == "l_hand":
            self.inventory.get_item(self.l_hand)
            self.l_hand = None
        elif slot == "rings":
            for ring in self.rings:
                self.inventory.get_item(ring)
            self.rings = MaxLenList(maxlen=2)
        elif slot == "all":
            for s in ('head', 'body', 'legs', 'r_hand', 'l_hand', 'rings'):
                self.de_equip(s)

    def serialize(self):
        def _g(slot):
            return slot.name if slot is not None else "empty"

        def _r(slot):
            return [item.name if item is not None else "empty" for item in slot]

        return {"head": _g(self.head),
                "body": _g(self.body),
                "legs": _g(self.legs),
                "r_hand": _g(self.r_hand),
                "l_hand": _g(self.l_hand),
                "rings": _r(self.rings)}

    def deserialize(self, data):
        def _d(data):
            return Item(data) if data != "empty" else None

        self.head = _d(data["head"])
        self.body = _d(data["body"])
        self.legs = _d(data["legs"])
        self.r_hand = _d(data["r_hand"])
        self.l_hand = _d(data["l_hand"])
        self.rings = MaxLenList(maxlen=2, iterable=[_d(d) for d in data["rings"]])


class Inventory:
    def __init__(self):
        self.items = []
        self.equipped = EquipmentInventory()
        self.money = 0

    def get_item(self, item):
        if isinstance(item, Item):
            item = item.name
        self.items.append(item)

    def remove_item(self, item):
        if isinstance(item, Item):
            item = item.name
        self.items.remove(item)

    def serialize(self):
        return {"items": self.items,
                "money": self.money,
                "equipped": self.equipped.serialize()}

    def deserialize(self, data):
        self.items = data["items"]
        self.money = data["money"]
        self.equipped.deserialize(data["equipped"])

    def equip_item(self, item):
        """Equips $item to the player"""
        if isinstance(item, str):
            item = Item(item)
        if item.equippable:
            self.equipped.equip(item)


class Stat:
    def __init__(self, value=0):
        self._value = value
        self.modifier = 0

    def randomize(self):
        self._value = sum([random.randint(1, 6) for i in range(3)])

    @property
    def value(self):
        return self._value + self.modifier

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

    def serialize(self):
        return [self._value, self.modifier]

    def deserialize(self, data):
        self._value, self.modifier = data


class PlayerStats:
    def __init__(self):
        self.str = Stat()
        self.int = Stat()
        self.dex = Stat()
        self.chr = Stat()
        self.con = Stat()
        self.wis = Stat()

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


class Player:
    def __init__(self, game):
        self.game = game
        self.name = None
        self._job = None
        self.experience = 0
        self._health = self.max_health
        self._mana = self.max_mana
        self.status_effects = []
        self.location = self.game.map.get_location_from_position((0, 0))
        self.inventory = Inventory()
        self.stats = PlayerStats()

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
