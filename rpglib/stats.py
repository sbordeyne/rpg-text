import random


class Stat:
    def __init__(self, value=10):
        self._value = value
        self.stat_modifier = 0

    def randomize(self):
        self._value = sum([random.randint(1, 6) for i in range(3)])

    @property
    def value(self):
        return self._value + self.stat_modifier

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

    def serialize(self):
        return [self._value, self.modifier]

    def deserialize(self, data):
        self._value, self.stat_modifier = data


class Stats:
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
