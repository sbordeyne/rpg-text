import json
from .utils import MaxLenList


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