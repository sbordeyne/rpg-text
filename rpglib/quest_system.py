class QuestState:
    def __init__(self, name):
        self.name = name
        self.next_states = {}
        pass

    def __eq__(self, other):
        if isinstance(other, QuestState):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other
        else:
            raise TypeError

    def trigger(self, trigger):
        next_state = self.next_states.get(trigger)
        return next_state

    @property
    def is_end_state(self):
        return not self.next_states


class Quest:
    def __init__(self, quest_log, name, variables=None):
        if variables is None:
            variables = {}
        self.quest_log = quest_log
        self.name = name
        self.state = None
        self.vars = variables

    def trigger(self, trigger):
        next_state = self.state.trigger(trigger)
        if next_state is not None:
            self.state = next_state
            if self.state.is_end_state:
                self.quest_log.finish_quest(self)

    def is_state(self, *states):
        for state in states:
            if self.state == state:
                return True
        return False


class QuestLog:
    def __init__(self, entity):
        self.entity = entity
        self.active_quests = {}
        self.completed_quests = []

    def get_quest(self, quest_name):
        if quest_name in self.active_quests.keys():
            return self.active_quests[quest_name]
        else:
            self.active_quests[quest_name] = Quest(self, quest_name)

    def finish_quest(self, quest):
        del self.active_quests[quest.name]
        self.completed_quests.append(quest)

    def is_quest_completed(self, quest_name):
        return quest_name in [q.name for q in self.completed_quests]
