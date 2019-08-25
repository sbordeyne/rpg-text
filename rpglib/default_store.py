import json


class DefaultStore:
    def __init__(self):
        self.defaults = {}
        with open("data/defaults.json") as f:
            data = json.load(f)

        self.defaults = data

    def __getattr__(self, item):
        try:
            return self.__dict__[item]
        except KeyError:
            return self.__dict__["defaults"].get(item)

    def __setattr__(self, key, value):
        if key in self.defaults.keys():
            self.defaults[key] = value
        else:
            self.__dict__[key] = value

    def __getitem__(self, item):
        return self.defaults.get(item)

    def get(self, data, category, item):
        return data.get(item, self[category][item])


default_store = DefaultStore()