class Command:
    def __init__(self, command, callback):
        self.command = command.lower()
        self.callback = callback

    def __call__(self, *args):
        self.callback(*args)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.command == other.lower()
        elif isinstance(other, Command):
            return self.command == other.command
        else:
            raise TypeError
    pass


class CommandSystem:
    def __init__(self, game):
        self.game = game
        self.commands = [Command("move", self.game.player.move),
                         Command("talk", self.game.character_system.talk),
                         Command("map", self.game.map.display),
                         Command("help", self.help),
                         Command("info", self.info),
                         Command("save", self.game.save_system.save),
                         Command("load", self.game.save_system.load),
                         Command("quit", self.game.quit),
                         Command("equip", self.game.player.inventory.equip_item),
                         Command("dequip", self.game.player.inventory.equipped.de_equip),
                         Command("rest", self.game.player.rest),
                         Command("inspect", self.game.player.inspect),
                         Command("use", self.game.player.use),
                         Command("view", self.game.player.view)]

        self.combat_commands = [Command("help", self.help_combat),
                                Command("flee", self.game.player.flee),
                                Command("attack", self.game.player.attack),
                                Command("cast", self.game.player.cast),
                                Command("use", self.game.player.use)]
        pass

    def parse(self, command):
        cmd, *cmd_args = command.split()
        for command in self.commands:
            if command == cmd:
                try:
                    rv = command(*cmd_args)
                except TypeError:
                    self.help(command)
                    return False
                return rv is None
        return False

    def parse_combat(self, command):
        cmd, *cmd_args = command.split()
        for command in self.combat_commands:
            if command == cmd:
                try:
                    rv = command(*cmd_args)
                except TypeError:
                    self.help_combat(command)
                    return False
                return rv is None
        return False

    def help(self, command=None):
        """Shows this message."""
        if command is None:
            for command in self.commands:
                print(f"{command.command} : {command.callback.__doc__}")
        else:
            print(f"{command.command} : {command.callback.__doc__}")

    def help_combat(self, command=None):
        """Shows this message"""
        if command is None:
            for command in self.combat_commands:
                print(f"{command.command} : {command.callback.__doc__}")
        else:
            print(f"{command.command} : {command.callback.__doc__}")

    def info(self, argument):
        """Gets information about $argument (location, player, npc, time)"""
        arg = argument.lower()
        if arg == "player":
            print(str(self.game.player))
        elif arg == "location":
            print(self.game.player.location.info())
        elif arg == "npc":
            print(self.game.character_system.info())
        elif arg == "time":
            print(self.game.timer.date)
        else:
            return False
