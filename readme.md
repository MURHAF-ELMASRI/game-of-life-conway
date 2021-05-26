# Game of life **conway** &nbsp;&nbsp;&nbsp; <img src="https://apprecs.org/gp/images/app-icons/300/30/com.gaurav.gameoflife.jpg" width='30'>

> The Game of Life, also known simply as Life, is a cellular automaton devised by the British mathematician John Horton Conway in 1970.It is a zero-player game, meaning that its evolution is determined by its initial state, requiring no further input. One interacts with the Game of Life by creating an initial configuration and observing how it evolves. It is Turing complete and can simulate a universal constructor or any other Turing machine.<br>[wikipedia](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)<br> > <br>

### This project is an Implementation of this game using **python** and **pygame**<br>

<br>
<img src="https://cdn3.iconfinder.com/data/icons/logos-and-brands-adobe/512/267_Python-512.png" width='100'> <img src="https://upload.wikimedia.org/wikipedia/commons/a/a9/Pygame_logo.gif" width='200'>
<br>
<br>
<img src="./20210526_150551.gif" width="400">
<br>
<br>

# Demo:

try demo demo of the application [click here]("./dist/")

# Rules 📏:

<br>[wikipedia](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)<br>

> The universe of the Game of Life is an infinite, two-dimensional orthogonal grid of square cells, each of which is in one of two possible states, live or dead, (or populated and unpopulated, respectively). Every cell interacts with its eight neighbours, which are the cells that are horizontally, vertically, or diagonally adjacent. At each step in time, the following transitions occur:

> 1.  Any live cell with fewer than two live neighbours dies, as if by underpopulation.
> 2.  Any live cell with two or three live neighbours lives on to the next generation.
> 3.  Any live cell with more than three live neighbours dies, as if by overpopulation.
> 4.  Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

> These rules, which compare the behavior of the automaton to real life, can be condensed into the following:

> Any live cell with two or three live neighbours survives.
> Any dead cell with three live neighbours becomes a live cell.
> All other live cells die in the next generation. Similarly, all other dead cells stay dead.
> The initial pattern constitutes the seed of the system. The first generation is created by applying the above rules simultaneously to every cell in the seed; births and deaths occur simultaneously, and the discrete moment at which this happens is sometimes called a tick. Each generation is a pure function of the preceding one. The rules continue to be applied repeatedly to create further generations.

# Project 📃 :

## [Game of life.py](<'./Game of life.py'>)

When I start developing the project I use brute force approach to make the game.<br>
Every Cell either 1: live or 0: die

## Algorithm 🧠:

-   loop over all cells
-   check the number of neighbor cells
-   if they apply rules listed above add the new state
-   display the new state of the board

## [dynamic_game_of_life.py]("./dynamic_game_of_life.py")

The game in the first program was too slow so I think why would I loop over all cells while I just need to check the live cells and the cells around it because no cells will come to life without a live cell beside it.<br>
And this what they called it **dynamic programming**

-   store live cell in an array
-   count the neighbor of the cells inside the array and in neighbor of the cells of the array
-   store the cells which apply the rules above.
-   display the result.

# installation 👷‍♂️:

It is assumed to have python program in your device if not check https://www.python.org/<br>

### open **cmd** and run the commands :

<br>

    git clone https://github.com/MURHAF-ELMASRI/game-of-life-conway.git
    cd game-of-life-conway
    python dynamic_game_of_life.py

# Pattern 😎 :

you can **open/save** the patters you have created.

### Check out interesting pattern the pattern file.

<br>

# Problem 🐛 **(SOLVED)** :

I tried to make .exe of this project to easy run it and play the game but I came across some bugs.
<br>
install pyinstaller from pip.

    pip install pyinstaller

after that try build the project

    pyinstaller --onefile dynamic_game_of_life.py

then you will see a dist folder have been created
open it and run the program.
<br>
Now you will see the the problem.

> In order to read the log of the problem open the program using cmd.

<br>

    font = pg.font.Font(pg.font.get_default_font, 15)

was the reason the the bug.
check the last version for working program.
