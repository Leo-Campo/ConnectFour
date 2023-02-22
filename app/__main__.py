import random
import sys
from .board import Board, BoardFullException, GameException
from loguru import logger


def _setup_logger(level: str):
    logger.remove()
    logger.add(sys.stdout, level=level)


if __name__ == "__main__":
    print("Welcome to your personal game of ConnectFour!")
    print("Here's the board you'll be playing on against me!")
    board = Board(7, 6)
    board.print_status()

    print("Good Luck!")

    # Game loop
    place = True
    game_over = False
    while True:
        column = input("Select a column: ")
        if column == "":
            continue
        ## Check for column to be an integer
        try:
            column = int(column)
        except ValueError as error:
            print(f"Column selection must be a positive integer in [1, {board.width}]")
            continue

        # Try to place a disc in the selected column
        try:
            game_over = board.place_disc(int(column) - 1, "player")
        except BoardFullException as draw:
            print("Looks like we ran out of space! Wanna play again?")
            sys.exit(0)
        except GameException as error:
            print(error.message)
            continue
        board.print_status()
        if game_over:
            print("!!!CONGRATULATIONS!!! You beat me")
            sys.exit(0)
        computerPlaced = False
        print("Now it's my turn! Take this!")
        while not computerPlaced:
            computer_column = random.choice(range(0, board.width))
            try:
                game_over = board.place_disc(computer_column, "computer")
                computerPlaced = True
            except BoardFullException as draw:
                print("Looks like we ran out of space! Wanna play again?")
                sys.exit(0)
            except GameException as error:
                continue
            board.print_status()
            if game_over:
                print("!!!AH AH I WON!!! Better luck next time!")
                sys.exit(0)
