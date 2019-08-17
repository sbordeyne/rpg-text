from lib.utils import sanitized_input
from lib.game import Game


def main():
    print("Welcome to rpg-text!")
    print("Please enter your character's name.")
    p_name = sanitized_input("> ", error_msg="")
    print("Please enter your desired job (commoner, spellcaster, warrior).")
    p_job = sanitized_input("> ", valid_input=('commoner', 'spellcaster', 'warrior'))
    game = Game(p_name, p_job)
    while True:
        game.next_turn()


if __name__ == '__main__':
    main()