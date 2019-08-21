from .utils import sanitized_input


class ShopSystem:
    def __init__(self, game):
        self.game = game
        self.in_shop = False

        self.welcome_message = 'Welcome into the shop!'  # Will be changed to a json read later on.

    def enter(self):
        self.in_shop = True
        print(self.welcome_message)
        while self.in_shop:
            command = sanitized_input("> ", error_msg="Invalid Command!")
            while not self.game.command_system.parse(command, command_set=self.game.command_system.shop_commands):
                print("Invalid command. Type 'help' for help.")
                command = sanitized_input("> ", error_msg="Invalid Command!")

    def buy(self, item):
        """Buy item $item."""
        pass

    def sell(self, item):
        """Sell item $item"""
        pass

    def exit(self):
        """Exit the shop"""
        self.in_shop = False

    def list(self, item=None):
        """List items for sale in the shop. Specify an $item to get more info about it."""
        pass
