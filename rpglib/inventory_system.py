from .utils import MaxLenList
from .item import Item
from collections import defaultdict
from .utils import parse_dice_format


class MoneyInventory:
    def __init__(self):
        self.coins = {
            "cc": 0,
            "sc": 0,
            "ec": 0,
            "gc": 0,
            "pc": 0,
        }
        self.gems = {
            "quartz": 0,
            "turquoise": 0,
            "onyx": 0,
            "garnet": 0,
            "amber": 0,
            "pearl": 0,
            "topaz": 0,
            "opal": 0,
            "ruby": 0,
            "diamond": 0,
        }
        self.jewels = {
            "bracelet": 0,
            "broach": 0,
            "necklace": 0,
            "crown": 0,
            "scepter": 0,
        }

    def __getitem__(self, item):
        if not isinstance(item, str):
            raise TypeError

        if item == "coins":
            return self.coins

        elif item == "gems":
            return self.gems

        elif item == "jewels":
            return self.jewels

        else:
            raise ValueError

    @property
    def coin_value(self):
        coeffs = {
            "cc": 0.01,
            "sc": 0.1,
            "ec": 0.5,
            "gc": 1,
            "pc": 5,
        }
        return sum([coeffs[k] * self.coins[k] for k in self.coins.keys()])

    @property
    def jewels_value(self):
        coeffs = {
            "bracelet": 300,
            "broach": 700,
            "necklace": 1100,
            "crown": 1500,
            "scepter": 1700,
        }
        return sum([coeffs[k] * self.jewels[k] for k in self.jewels.keys()])

    @property
    def gems_value(self):
        coeffs = {
            "quartz": 10,
            "turquoise": 10,
            "onyx": 50,
            "garnet": 150,
            "amber": 100,
            "pearl": 500,
            "topaz": 600,
            "opal": 1000,
            "ruby": 1500,
            "diamond": 2500,
        }
        return sum([coeffs[k] * self.gems[k] for k in self.gems.keys()])

    @property
    def value(self):
        return self.coin_value + self.jewels_value + self.gems_value

    def serialize(self):
        return {
            "coins": self.coins,
            "jewels": self.jewels,
            "gems": self.gems,
        }

    def deserialize(self, data):
        self.coins = data["coins"]
        self.jewels = data["jewels"]
        self.gems = data["gems"]

    def get_gem(self, *gem_names):
        for gem_name in gem_names:
            if gem_name in self.gems.keys():
                self.gems[gem_name] += 1

    def get_jewel(self, *jewel_names):
        for jewel_name in jewel_names:
            if jewel_name in self.jewels.keys():
                self.jewels[jewel_name] += 1

    def get_coins(self, coin_name, coin_amount=1):
        self.coins[coin_name] += coin_amount

    def update(self, key, value):
        if key == "coins":
            for coin_type, coin_amount in value.items():
                self.get_coins(coin_type, coin_amount)
        elif key == "jewels":
            self.get_jewel(*value)
        elif key == "gems":
            self.get_gem(*value)

    def get_random_starting_money(self):
        self.coins["gc"] = parse_dice_format('29d6')
        self.coins["cc"] = parse_dice_format('d100')
        self.coins["sc"] = parse_dice_format('d100')
        self.coins["ec"] = parse_dice_format('d100')


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

    def get_total_ac(self):
        ac = 0
        def _ac(slot):
            if slot:
                return slot.ac_bonus
            return 0
        
        ac += _ac(self.head)
        ac += _ac(self.body)
        ac += _ac(self.legs)
        ac += _ac(self.r_hand)
        ac += _ac(self.l_hand)
        for ring in self.rings:
            ac += _ac(ring)
        return ac

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

    @property
    def as_dict(self):
        def _g(slot):
            return slot.display_name if slot is not None else "empty"

        return {"head": _g(self.head),
                "body": _g(self.body),
                "legs": _g(self.legs),
                "r.hand": _g(self.r_hand),
                "l.hand": _g(self.l_hand),
                "rings": [item.name if item is not None else "empty" for item in self.rings]}

    def serialize(self):
        def _g(slot):
            return slot.name if slot is not None else "empty"

        return {"head": _g(self.head),
                "body": _g(self.body),
                "legs": _g(self.legs),
                "r_hand": _g(self.r_hand),
                "l_hand": _g(self.l_hand),
                "rings": [item.name if item is not None else "empty" for item in self.rings]}

    def deserialize(self, data):
        def _d(d):
            return Item(d) if d != "empty" else None

        self.head = _d(data["head"])
        self.body = _d(data["body"])
        self.legs = _d(data["legs"])
        self.r_hand = _d(data["r_hand"])
        self.l_hand = _d(data["l_hand"])
        self.rings = MaxLenList(maxlen=2, iterable=[_d(d) for d in data["rings"]])


class Inventory:
    def __init__(self):
        self.items = defaultdict(int)
        self.equipped = EquipmentInventory(self)
        self.money = MoneyInventory()

    def get_item(self, item):
        if isinstance(item, Item):
            item = item.name
        self.items[item] += 1

    def remove_item(self, item):
        if isinstance(item, Item):
            item = item.name
        self.items[item] -= 1
        if self.items[item] == 0:
            del self.items[item]

    def has_item(self, item):
        if isinstance(item, Item):
            item = item.name
        return item in self.items and self.items[item] > 0

    def use_item(self, item, target=None):
        if self.has_item(item):
            if isinstance(item, str):
                item = Item(item)
            item.use(target)

    def serialize(self):
        return {"items": self.items,
                "money": self.money.serialize(),
                "equipped": self.equipped.serialize()}

    def deserialize(self, data):
        self.items = data["items"]
        self.money.deserialize(data["money"])
        self.equipped.deserialize(data["equipped"])

    def equip_item(self, item):
        """Equips $item to the player"""
        if isinstance(item, str):
            item = Item(item)
        if item.equippable:
            self.equipped.equip(item)