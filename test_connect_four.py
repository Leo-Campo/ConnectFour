from connect_four import Board, BoardFullException, FullColumnException
import pytest


def create_board():
    board = Board(7, 6)
    return board


def fill_board(board, cells, char):
    """Auxiliary method to build a board in a certain state

    Fills the board using the coordinates in cells with character char
    """
    for x, y in cells:
        board.board[y][x] = char
    return board


def test_place_discs():
    """Tests placing a disc works as intended, placing the disc on the lower possible slot of a given column"""
    board = create_board()
    # Test 3 horizontal, 3 vertical placements
    board.place_disc(0, "player")
    board.place_disc(1, "player")
    board.place_disc(2, "player")

    board.place_disc(0, "player")
    board.place_disc(0, "player")

    board.place_disc(1, "player")

    test_board = create_board()
    test_board = fill_board(
        board, [(5, 0), (5, 1), (5, 2), (4, 0), (3, 0), (4, 1)], test_board.player_char
    )

    assert board.board == test_board.board


def test_board_is_full():
    """Tests the board is not recognized as full for all width * height -1 disc placements"""
    board = create_board()
    for insertion in range(0, board.width * board.height):
        board.place_disc(insertion % 7, "player" if insertion % 2 == 0 else "computer")
    assert board.is_full()


def test_board_is_not_full():
    """Tests the board is not recognized as full for all width * height -1 disc placements"""
    board = create_board()
    for insertion in range(0, board.width * board.height - 1):
        board.place_disc(insertion % 7, "player" if insertion % 2 == 0 else "computer")
    assert not board.is_full()


def test_draw():
    """Fills the board in a draw state and tests the game is recognized as a draw

    The example draw board is as follows (X player, O computer):
    OXOXOXO
    OXOXOXO
    OXOXOXO
    XOXOXOX
    XOXOXOX
    XOXOXOX
    """
    board = create_board()
    player_cells = [
        (0, 3),
        (0, 4),
        (0, 5),
        (1, 0),
        (1, 1),
        (1, 2),
        (2, 3),
        (2, 4),
        (2, 5),
        (3, 0),
        (3, 1),
        (3, 2),
        (4, 3),
        (4, 4),
        (4, 5),
        (5, 0),
        (5, 1),
        (5, 2),
        (6, 3),
        (6, 4),
        (6, 5),
    ]
    board = fill_board(board, player_cells, "X")

    computer_cells = [
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 3),
        (1, 4),
        (1, 5),
        (2, 0),
        (2, 1),
        (2, 2),
        (3, 3),
        (3, 4),
        (3, 5),
        (4, 0),
        (4, 1),
        (4, 2),
        (5, 3),
        (5, 4),
        (5, 5),
        (6, 0),
        (6, 1),
    ]

    board = fill_board(board, computer_cells, "O")
    with pytest.raises(BoardFullException) as draw:
        board.place_disc(6, "computer")


def test_win_horizontally():
    """Tests the player wins the game horizontally"""
    board = create_board()
    game_over = board.place_disc(0, "player")
    assert not game_over

    game_over = board.place_disc(1, "player")
    assert not game_over

    game_over = board.place_disc(2, "player")
    assert not game_over

    game_over = board.place_disc(3, "player")
    assert game_over


def test_win_vertically():
    """Tests the player wins the game vertically"""
    board = create_board()
    game_over = board.place_disc(0, "player")
    assert not game_over

    game_over = board.place_disc(0, "player")
    assert not game_over

    game_over = board.place_disc(0, "player")
    assert not game_over

    game_over = board.place_disc(0, "player")
    assert game_over


def test_win_diagonally_right():
    """Tests the player wins the game diagonally from upper right to lower left"""
    board = create_board()
    game_over = board.place_disc(0, "player")
    assert not game_over

    game_over = board.place_disc(1, "computer")
    assert not game_over

    game_over = board.place_disc(1, "player")
    assert not game_over

    game_over = board.place_disc(2, "computer")
    assert not game_over

    game_over = board.place_disc(2, "computer")
    assert not game_over

    game_over = board.place_disc(2, "player")
    assert not game_over

    game_over = board.place_disc(3, "computer")
    assert not game_over

    game_over = board.place_disc(3, "computer")
    assert not game_over

    game_over = board.place_disc(3, "computer")
    assert not game_over

    game_over = board.place_disc(3, "player")
    assert game_over


def test_win_diagonally_left():
    """Tests the player wins the game diagonally from upper left to lower right"""
    board = create_board()
    game_over = board.place_disc(3, "player")
    assert not game_over

    game_over = board.place_disc(2, "computer")
    assert not game_over

    game_over = board.place_disc(2, "player")
    assert not game_over

    game_over = board.place_disc(1, "computer")
    assert not game_over

    game_over = board.place_disc(1, "computer")
    assert not game_over

    game_over = board.place_disc(1, "player")
    assert not game_over

    game_over = board.place_disc(0, "computer")
    assert not game_over

    game_over = board.place_disc(0, "computer")
    assert not game_over

    game_over = board.place_disc(0, "computer")
    assert not game_over

    game_over = board.place_disc(0, "player")
    assert game_over