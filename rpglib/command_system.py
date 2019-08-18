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
                         Command("dequip", self.game.player.inventory.equipped.de_equip)]
        pass

    def parse(self, command):
        cmd, *cmd_args = command.split()
        for command in self.commands:
            if command == cmd:
                try:
                    rv = command(*cmd_args)
                except TypeError:
                    return False
                return rv is None
        return False

    def help(self):
        """Shows this message."""
        for command in self.commands:
            print(f"{command.command} : {command.callback.__doc__}")

    def info(self, argument):
        """Gets information about $argument (location, player, npc)"""
        arg = argument.lower()
        if arg == "player":
            print(str(self.game.player))
        elif arg == "location":
            print(self.game.player.location.info())
        elif arg == "npc":
            print(self.game.character_system.info())
        else:
            return False
