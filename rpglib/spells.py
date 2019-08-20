import json
from .utils import parse_dice_format, interpolate_brackets


class Spell:
    def __init__(self, name, spelldata):
        self.name = name
        self.targetable, self.type = spelldata["type"].split("/")
        if self.type == "damage":
            self.damage_roll = spelldata["damage"]
        self.level = spelldata["level"]
        self.job = spelldata["job"]
        self.effects = list(spelldata.get("effects", []))
        self.description = spelldata.get("description", None)
        self.cost = spelldata.get("cost", 5)

    def damage(self, caster):
        roll = self.damage_roll
        if "lvl" in self.damage_roll:
            roll = roll.replace("lvl", str(caster.level))
        return parse_dice_format(roll) + caster.stats.int.modifier

    def cast(self, caster, target):
        if caster.job.name == self.job and caster.mana >= self.cost:
            amount = 0
            if self.type == "damage":
                amount = self.damage(caster)
                target.take_damage(amount)
                target.apply_status_effects(*self.effects)
            elif self.type == "heal":
                amount = self.damage(caster)
                target.heal(amount)
                target.apply_status_effects(*self.effects)
            elif self.type == "buff":
                target.apply_status_effects(*self.effects)

            caster.mana -= self.cost
            self.display_description(caster, target, amount)
        elif caster.mana < self.cost:
            print("You don't have enough mana to cast this spell.")
        else:
            print(f"This spelled can't be casted by {caster.job.name.capitalize()}s!")

    def display_description(self, caster, target, amount=0):
        if self.description is not None:
            print(interpolate_brackets(self.description, caster=caster.name.capitalize(),
                                       target=target.name.capitalize(), amount=amount))


class SpellList:
    def __init__(self, entity):
        self.entity = entity
        with open("data/spells.json") as f:
            data = json.load(f)
        for key in data.keys():
            self.__dict__[key] = Spell(key, data[key])

    def cast(self, spell, target):
        if spell in self.__dict__.keys():
            self.__dict__[spell].cast(self.entity, target)
