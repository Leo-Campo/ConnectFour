import random
import sys


class GameException(Exception):
    "Raised when an error occurs during the game"

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class FullColumnException(GameException):
    "Raised when a full column is selected"

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class ColumnOutOfBoundsException(GameException):
    "Raised when a column number out of bounds is selected"

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class BoardFullException(GameException):
    "Raised when the board runs out of space"

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class Board:
    """
    Board where a ConnectFour game takes place
    """

    DIRECTION_OFFSET = {
        "LEFT": (0, -1),
        "RIGHT": (0, 1),
        "UP": (-1, 0),
        "DOWN": (1, 0),
        "UPPER_LEFT": (-1, -1),
        "UPPER_RIGHT": (-1, 1),
        "LOWER_LEFT": (1, -1),
        "LOWER_RIGHT": (1, 1),
    }  # Offsets used for directional winning condition checks

    def __init__(self, width, height):
        self.neutral_char = "-"  # Char used for empty slots
        self.player_char = "X"  # Char used for player occupied slots
        self.computer_char = "O"  # Char used for computer occupied slots

        self.width = width
        self.height = height
        self.board = [[self.neutral_char for i in range(width)] for j in range(height)]

        self.char_map = {"player": self.player_char, "computer": self.computer_char}

    def _get_disc_by_direction(self, x, y, direction_x, direction_y):
        """
        Returns the disc obtained by moving from slot (x, y) through direction (direction_x, direction_y)
        Returns None if movement ends out of bounds
        """
        try:
            if x + direction_x >= 0 and y + direction_y >= 0:
                return self.board[x + direction_x][y + direction_y]
            else:
                return None
        except Exception:
            return None

    def _count_discs(
        self, char, new_disc_x, new_disc_y, direction_x, direction_y, threshold=4
    ):
        """
        Counts how many discs of the same starting one char are met consecutively from starting position
        (new_disc_x, new_disc_y) moving through direction (direction_x, direction_y)

        Counts up to 4 consecutive discs, as 4 equal discs are enough to declare a winner (in a
        connect_four game, the threshold may be changed for different games)
        """
        count = 0
        for step in range(1, threshold):
            if (
                self._get_disc_by_direction(
                    new_disc_x, new_disc_y, direction_x * step, direction_y * step
                )
                == char
            ):
                count += 1
            else:
                break
        return count

    def _count_discs_by_directions_pairs(
        self, char, new_disc_x, new_disc_y, first_direction_key, second_direction_key
    ):
        """
        Counts discs equal to char encountered by moving on the board in the directions pairs.

        Returns the number of equal discs consecutively met
        """
        if (
            first_direction_key not in self.DIRECTION_OFFSET.keys()
            or second_direction_key not in self.DIRECTION_OFFSET.keys()
        ):
            # Invalid directons selected
            return 0

        direction_x, direction_y = self.DIRECTION_OFFSET[first_direction_key]
        first_count = self._count_discs(
            char, new_disc_x, new_disc_y, direction_x, direction_y
        )

        direction_x, direction_y = self.DIRECTION_OFFSET[second_direction_key]
        second_count = self._count_discs(
            char, new_disc_x, new_disc_y, direction_x, direction_y
        )

        return first_count + second_count + 1

    def is_game_won(self, new_disc_x, new_disc_y):
        """
        Checks if the disc inserted at (new_disc_x, new_disc_y) causes the player to win the game

        Computation is made by counting discs in all directions in pairs. If the number of counted discs is 4 or more,
        counting the starting disc too, the current player has won the game
        """
        current_char = self.board[new_disc_x][new_disc_y]
        # Check for directions in pairs (left, right), (up, down), (upper left, lower right), (upper right, lower left)

        #! Left - Right
        count = self._count_discs_by_directions_pairs(
            current_char, new_disc_x, new_disc_y, "LEFT", "RIGHT"
        )
        if count >= 4:
            return True

        #! Up - Down
        count = self._count_discs_by_directions_pairs(
            current_char, new_disc_x, new_disc_y, "UP", "DOWN"
        )

        if count >= 4:
            return True

        #! Upper Left - Lower Right
        count = self._count_discs_by_directions_pairs(
            current_char, new_disc_x, new_disc_y, "UPPER_LEFT", "LOWER_RIGHT"
        )

        if count >= 4:
            return True

        #! Upper Right - Lower Left
        count = self._count_discs_by_directions_pairs(
            current_char, new_disc_x, new_disc_y, "UPPER_RIGHT", "LOWER_LEFT"
        )
        if count >= 4:
            return True

        # Else game is not over yet
        return False

    def is_full(self):
        """Returns true if the board has run out of space"""
        for row in self.board:
            for cell in row:
                if cell == self.neutral_char:
                    return False
        return True

    def place_disc(self, x, player_key):
        """
        Places a disc on the board

        Each disc placement triggers a check to determine whether the game is over or still going
        """
        if x < 0 or x >= self.width or x is None or x == "":
            raise ColumnOutOfBoundsException("Column selected is not valid")
        else:
            added = False
            new_disc_x, new_disc_y = 0, 0
            for idx in range(self.height - 1, -1, -1):
                if self.board[idx][x] == self.neutral_char:
                    self.board[idx][x] = self.char_map[player_key]
                    added = True
                    new_disc_x = idx
                    new_disc_y = x
                    break
                else:
                    continue
            if added:
                if not self.is_game_won(new_disc_x, new_disc_y):
                    if self.is_full():
                        raise BoardFullException("Board has run out of space")
                    else:
                        return False
                else:
                    return True
            else:
                raise FullColumnException("Column selected is full")

    def print_status(self):
        """
        Prints the current board status
        """
        print("*" * 5 * self.width)
        [print(row) for row in self.board]
        print("*" * 5 * self.width)


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
            print("!!!CONGRATULATIONS!!! You beated me")
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
