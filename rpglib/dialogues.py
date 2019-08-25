import json
from .default_store import default_store


class Dialogue:
    def __init__(self, dialogue_id):
        self.dialogue_id = dialogue_id

        with open('data/dialogues.json') as f:
            data = json.load(f)

        self.dialogue = data.get('dialogue', default_store.dialogues['dialogue'])
        self.choices = data.get('choices', default_store.choices['choices'])
        self.choices = {cname: Dialogue(c) for (cname, c) in self.choices}

    def __call__(self, *args, **kwargs):
        for (who, what) in self.dialogue:
            yield who, what

        for choice in self.choices.keys():
            yield 'choice', choice

    def choose_choice(self, choice):
        return self.choices.get(choice)
