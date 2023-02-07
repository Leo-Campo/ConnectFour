# ConnectFour
To play a game of connect four, just run the connect_four.py script from the command line (assuming python3 is installed).

python3 connect_four.py

The game will begin immediately, with the player being asked to select a column and the computer making its move. Once the player or the computer places a winning disc, the game ends and the script terminates. The same happens when the whole board is full, ending the game in a draw. The game takes place as a whole on the command line

The game is created with minimal library usage: sys to exit the program once the game ends with an error code of 0 (no errors) and random to make the computer place a disc randomly. 

The program contains a main class, Board, that encodes the playing board and all additional data such as characters used, control flags and all methods needed to interact with it. The main game loop handles player input and the game state.

Methods in the Board class raise exceptions, declared outside of the Board class (but in the same file). These exceptions are catched in the main game loop to recognize certain situations, such as a column selected being full or the game being over with no winner.

The program comes with a suite of tests to make sure methods are working as intended. These tests cases are collected in the test_connect_four.py script and are written using the pytest framework. Such framework can be install as any other python package with

pip install pytest

Once the framework is installed, tests can be run simply with the command 

pytest

Optionally, you can pass the -v argument to pytest to obtain a more verbose output

