from rpglib.game import Game


def main():
    game = Game()
    game.main_menu()
    while True:
        game.next_turn()


if __name__ == '__main__':
    main()