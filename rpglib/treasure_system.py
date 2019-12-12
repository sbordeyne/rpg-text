import json
from .utils import parse_dice_format
import random


class LootTable:
    def __init__(self, loot_type):
        self.type = loot_type
        with open("data/loot_tables.json") as f:
            self.data = json.load(f).get(loot_type, {})

    @property
    def get(self):
        n = random.randint(1, 100)
        for key, value in self.data.items():
            min_n, max_n = key.split("-")
            min_n = int(min_n)
            max_n = int(max_n)
            if min_n <= n <= max_n:
                return random.choice(list(value))


class ItemsLootTable:
    def __init__(self, loot_type):
        self.type = loot_type
        with open("data/loot_tables.json") as f:
            self.data = json.load(f)["items"]

    @property
    def get(self):
        if "random" in self.type:
            exceptions = self.type.split("|")[1:]
            loot_type = "/".join([k for k in self.data.keys() if k not in exceptions])
        else:
            loot_type = self.type
        loot_type = random.choice(loot_type.split("/"))
        data = self.data.get(loot_type, {})
        n = random.randint(1, 100)
        for key, value in data.items():
            min_n, max_n = key.split("-")
            min_n = int(min_n)
            max_n = int(max_n)
            if min_n <= n <= max_n:
                return random.choice(list(value))


class Treasure:
    def __init__(self, treasure_type):
        with open("data/treasures.json") as f:
            data = json.load(f).get(treasure_type, {})
        self.coins = data.get("coins", ["0%", ""])
        self.gems = data.get("gems", ["0%", ""])
        self.jewels = data.get("jewels", ["0%", ""])
        self.average_value = data.get("average_value", 0)
        self.items = data.get("items", ["0%", ""])
        self.multiplier = 1000 if data.get("thousands", False) else 1

    def calculate(self):
        coin_rv = {}
        gem_rv = []
        jewels_rv = []
        item_rv = []

        for coin, coin_data in self.coins.items():
            if Treasure.has_item(coin_data[0]):
                coin_rv[coin] = parse_dice_format(coin_data[1]) * self.multiplier

        if Treasure.has_item(self.gems[0]):
            gems_lt = LootTable("gems")
            n_gems = parse_dice_format(self.gems[1])
            for i in range(n_gems):
                gem_rv.append(gems_lt.get)

        if Treasure.has_item(self.jewels[0]):
            jewels_lt = LootTable("jewels")
            n_jewels = parse_dice_format(self.jewels[1])
            for i in range(n_jewels):
                jewels_rv.append(jewels_lt.get)

        if Treasure.has_item(self.items[0]):
            for loot_type in self.items[1]:
                if ":" in loot_type:
                    roll, table = loot_type.split(":")
                    for i in range(parse_dice_format(roll)):
                        items_lt = ItemsLootTable(table)
                        item_rv.append(items_lt.get)
                else:
                    items_lt = ItemsLootTable(loot_type)
                    item_rv.append(items_lt.get)

        return {"coins": coin_rv,
                "gems": gem_rv,
                "jewels": jewels_rv,
                "items": item_rv}

    @staticmethod
    def has_item(percent):
        percent = int(percent.replace(" ", "").replace("%", ""))
        return random.randint(1, 100) < percent


class TreasureSystem:
    def __init__(self, game):
        self.game = game
        pass

    @staticmethod
    def get_treasure(treasure_type):
        return Treasure(treasure_type)

    def add_treasure(self, treasure_type):
        player = self.game.player
        treasure = TreasureSystem.get_treasure(treasure_type).calculate().items()
        for k, v in treasure:
            if k != "items":
                player.inventory.money.update(k, v)
            elif k == "items":
                for item in v:
                    player.inventory.get_item(item)
        return treasure
