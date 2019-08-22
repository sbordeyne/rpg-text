class Command:
    def __init__(self, command, callback, command_args=None):
        self.command = command.lower()
        self.callback = callback
        self.command_args = command_args if command_args is not None else {}

    def __call__(self, *args):
        self.callback(*args, **self.command_args)

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
                         Command("view", self.game.player.view),
                         Command("enter", self.game.enter)]

        self.combat_commands = [Command("help", self.help_combat),
                                Command("flee", self.game.player.flee),
                                Command("attack", self.game.player.attack),
                                Command("cast", self.game.player.cast),
                                Command("use", self.game.player.use)]

        self.shop_commands = [Command("help", self.help_shop),
                              Command("buy", self.game.shop_system.buy),
                              Command("sell", self.game.shop_system.sell),
                              Command("list", self.game.shop_system.list),
                              Command("exit", self.game.shop_system.exit)]
        pass

    def parse(self, command, command_set=None):
        cmd, *cmd_args = command.split()
        if command_set is None:
            command_set = self.commands
        for command in command_set:
            if command == cmd:
                try:
                    rv = command(*cmd_args)
                except TypeError:
                    self.help(command)
                    return False
                return rv is None
        return False

    def help(self, command=None, command_set=None):
        """Shows this message."""
        if command_set is None:
            command_set = self.commands

        if isinstance(command, str):
            for com in command_set:
                if com.command == command:
                    command = com
                    break
                else:
                    command = None

        if command is None:
            for command in command_set:
                print(f"{command.command} : {command.callback.__doc__}")
        else:
            print(f"{command.command} : {command.callback.__doc__}")

    def help_combat(self, command=None):
        """Shows this message."""
        self.help(command, command_set=self.combat_commands)

    def help_shop(self, command=None):
        """Shows this message."""
        self.help(command, command_set=self.shop_commands)

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
