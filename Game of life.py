""""
Game of life by conway Is nice simple game have 4 rule.Imagine we play on bord have cells , every cell has two conditions live our die.
1: If a cell have 0  , 1   , 2 or more than 3 neighbor cells it will die
2: If a cell have have exactly 3 neighbor cells  will live

note : to remained myself : I used thread when I user click start button to run the main_game
Because it is my first project in pygamge : there are some bad implementation of pygame function and needless reusing it. I don't want to consume some time reediting it>
"""

import threading

import pygame as pg
import time
import pygame.locals as ls
import pygame

class button():  # define button class to save time from reiniate the button
    def __init__(self, x, y, width, length, text):
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.text = text
    # draw the button >> note>> posx and posy used to draw the button more darker if I hover over it
    def draw_button(self, screen, posx, posy):
        if (self.ishover(posx, posy)):
            pg.draw.rect(screen, (100, 100, 100), [self.x, self.y, self.width, self.length], 0)
        else:
            pg.draw.rect(screen, (200, 200, 200), [self.x, self.y, self.width, self.length], 0)
        font = pg.font.Font(pg.font.get_default_font(), 15)
        txt = font.render(str(self.text), True, (255, 255, 255))
        screen.blit(txt, (
            self.x + (self.width / 2 - txt.get_width() / 2), self.y + (self.length / 2 - txt.get_height() / 2)))
    # return True if the mouse hover over it
    def ishover(self, posx, posy):
        if (posx >= self.x and posx <= self.x + self.width and posy >= self.y and posy <= self.y + self.length):
            return True
        return False
    # return True if the button is clicked
    def isclicked(self, posx, posy):
        if (posx >= self.x and posx <= self.x + self.width and posy >= self.y and posy <= self.y + self.width):
            return True
        return False

#the cell have value of 0 if it is die and 1 if it is alive
class cells():
    def __init__(self, x=0, y=0, width=0):
        self.x = x
        self.y = y
        self.width = width
        self.value = 0
    # draw black square if it is die
    def drew(self, surface):
        if (self.value == 0):
            pg.draw.rect(surface, (0, 0, 0), [self.x, self.y, self.width, self.width], 0)
    # White square if it alive
        if (self.value == 1):
            pg.draw.rect(surface, (255, 255, 255), [self.x, self.y, self.width, self.width], 0)
    #used this fucntion as subfunction for select_sq
    def fill(self, surface):
        self.value = 1
        self.drew(surface)

# to check out if it is allow for the scan function to see the available cell >> to not cause a OUT OF RANGE error
def bondryx(j, n):
    return (j < n and j >= 0)

# same function but fro y axies
def bondryy(i, n):
    return (i < n and i >= 0)

# this method is the core of the game, it is implement the rule mentioned before on the cell>
# it represents one generation of the game

def scan(cells):
    i, j = 0, 0
    dx = [-1, 0, 1, 1, 1, 0, -1, -1]
    dy = [-1, -1, -1, 0, 1, 1, 1, 0]
    ref = [[cells[i][j].value for j in range(len(cells[0]))] for i in range(len(cells))] # reference for the cells to compare with the first mode of the neighbor cell
    x = len(cells[0])
    y = len(cells)
    while i < y:
        j = 0
        while j < x:
            nib = 0
            for k in range(8):
                if (bondryy(i + dy[k], y) and bondryx(j + dx[k], x)):

                    if (ref[i + dy[k]][j + dx[k]] == 1):
                        nib += 1
            if (cells[i][j].value == 1):
                if (nib == 1 or nib == 0):
                    cells[i][j].value = 0
                elif (nib == 2 or nib == 3):
                    cells[i][j].value = 1
                elif nib >= 4:
                    cells[i][j].value = 0
            elif (cells[i][j].value == 0):
                if nib == 3:
                    cells[i][j].value = 1
            j += 1
        i += 1
    return cells

#main_game to continue play the game as far as there is an alive cell
def main_game(cell, stop):
    x = len(cell[0])
    y = len(cell)
    sleep_t=0.005
    while (True):
        light = False
        for i in range(y):
            for j in range(x):  # Attintion: this two loop apply to just check out weather all cells are empty or not
                if (cell[i][j].value == 1):
                    light = True
                    break
            if (light):
                break

        if (light):
            cell = scan(cell)
            time.sleep(sleep_t)

        if (stop()):        # this implementation used to pass a value to stop the thread
            break



def writecells(screen, cell):   # draw the cells
    x = len(cell[0])
    y = len(cell)
    for i in range(y):
        for j in range(x):
            cell[i][j].drew(screen)

#iniat the cells in the begging of the game
#here ther is a bad implementation
#this fuction will iniat 20 * 20 cells if the window is small and 144* 64 if the window is large
def init_cells(large_screen, small):
    x, y = 2, 2
    i, j = 0, 0
    if (442 >= large_screen):
        if (small):
            cell = [[cells() for _ in range(40)] for _ in range(40)]
            for i in range(40):
                x = 1
                for j in range(40):
                    cell[i][j] = cells(x, y, 10)
                    x = x + 11
                y = y + 11

        else:
            cell = [[cells() for _ in range(20)] for _ in range(20)]
            for i in range(20):
                x = 2
                for j in range(20):
                    cell[i][j] = cells(x, y, 20)
                    x = x + 22
                y = y + 22

    else:
        if (small):
            cell = [[cells() for _ in range(114)] for _ in range(64)]
            for i in range(64):
                x = 1
                for j in range(114):
                    cell[i][j] = cells(x, y, 10)
                    x = x + 11
                y = y + 11
        else:
            cell = [[cells() for _ in range(57)] for _ in range(32)]
            for i in range(32):
                x = 2
                for j in range(57):
                    cell[i][j] = cells(x, y, 20)
                    x = x + 22
                y = y + 22

    return cell

#draw a transparente red square when the crouser move around
def hover(screen, posx, posy, small):
    if (posx < screen.get_width() - 112 and posy < screen.get_height() - 1):
        if not small:
            x = posx // 22
            x = x * 22
            y = posy // 22
            y = y * 22
            s = pg.Surface((20, 20))
            s.set_alpha(200)
            s.fill((255, 0, 0))
            screen.blit(s, (x + 2, y + 2))
            return True
        else:
            x = posx // 11
            x = x * 11
            y = posy // 11
            y = y * 11
            s = pg.Surface((10, 10))
            s.set_alpha(200)
            s.fill((255, 0, 0))
            screen.blit(s, (x + 1, y + 1))
            return True

    return False

# return the value of the cells to 0
def clean_cell(cell, posx, posy, small):
    if small:
        x = posx // 11
        y = posy // 11
    else:
        x = posx // 22
        y = posy // 22
    cell[y][x].value = 0
    return cell

# blow the cell up and turn its value to 1
def select_sq(cell, posx, posy, small):
    if small:
        x = posx // 11
        y = posy // 11
    else:
        x = posx // 22
        y = posy // 22
    cell[y][x].value = 1
    return cell

#return all the value of the cells to 0
def clean_allcells(cell):
    x = len(cell[0])
    y = len(cell)
    for i in range(y):
        for j in range(x):
            cell[i][j].value = 0
    return cell

#backgound is created of the sqaure table
def drew_background(surface, cell):
    x = len(cell[0])
    y = len(cell)
    surface.fill((255, 255, 255))
    for i in range(y):
        for j in range(x):
            pg.draw.rect(surface, (0, 0, 0), [cell[i][j].x, cell[i][j].y, cell[i][j].width, cell[i][j].width], 0)


#diplay the window
def main():
    #display the window
    pg.init()
    screen = pg.display.set_mode((550, 442), pg.RESIZABLE)
    #initiate some variable
    small_cell = False
    font = pg.font.Font(pg.font.get_default_font(), 10)
    press = False   # to check if the the right mouse has clicked
    going = True   # stop while
    hide = True    # hide the background
    start = False   # start the main game
    size_text = font.render("cell size ", True, (255, 255, 255))   # give the user tow option for cells' size
    background_cell = pg.Surface((screen.get_width() - 108, screen.get_height()))


    while going:
        screen.fill((0, 0, 0))
        posx, posy = pg.mouse.get_pos()  # get the position of the mouse

        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False

            if event.type == pg.VIDEORESIZE:             # is work when the window is resized
                screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
                print(screen)
                cell = init_cells(screen.get_height(), small_cell)
                background_cell = pg.Surface((screen.get_width() - 108, screen.get_height()))
                drew_background(background_cell, cell)
                start_button = button(screen.get_width() - 100, screen.get_height() - 330, 90, 60, "start")
                hide_line = button(screen.get_width() - 100, screen.get_height() - 230, 90, 60, "Hide line")
                clean_button = button(screen.get_width() - 100, screen.get_height() - 130, 90, 60, "Clean")
                big_button = button(screen.get_width() - 50, screen.get_height() - 400, 45, 30, "Big")
                small_button = button(screen.get_width() - 100, screen.get_height() - 400, 45, 30, "small")


                x_crouser_text = screen.get_width() - 100
                y_crouser_text = screen.get_height() - 40

                size_text_x = screen.get_width() - 75
                size_text_y = screen.get_height() - 430



                game_thread = threading.Thread(target=main_game, args=(cell, lambda: stop_threads), daemon=True) # creat thread of the main game and pass stop threads as varibale to control its functioninig
                stop_threads=False
            elif event.type == pg.MOUSEBUTTONDOWN:
                press = event.button # get the input value

                # check the buttons clicking
                if(press==1 and small_button.isclicked(posx,posy)):
                    small_cell=True
                    cell=init_cells(screen.get_height(),small_cell)
                    drew_background(background_cell, cell)


                if(press==1 and big_button.isclicked(posx,posy)):
                    small_cell=False
                    cell=init_cells(screen.get_height(),small_cell)
                    drew_background(background_cell, cell)

                if (press == 1 and hide_line.isclicked(posx, posy)):
                    hide = False if (hide) else True

                if (press == 1 and start_button.isclicked(posx, posy)):
                    if start:
                        start = False
                        start_button.text = "Run"
                        stop_threads = True
                    else:
                        stop_threads=False
                        start = True
                        start_button.text = "Stop"

                if (press == 1 and clean_button.isclicked(posx, posy)):
                    cell = clean_allcells(cell)
                    start = False
                    start_button.text = "Run"
                    stop_threads = True

            elif event.type == pg.MOUSEBUTTONUP:
                press = 0

        # draw the buttons
        clean_button.draw_button(screen, posx, posy)
        hide_line.draw_button(screen, posx, posy)
        start_button.draw_button(screen, posx, posy)
        big_button.draw_button(screen, posx, posy)
        small_button.draw_button(screen, posx, posy)
        #space_button.draw_button(screen,posx,posy)
        # hide of show the background
        if (hide):
            screen.blit(background_cell, (0, 0))
            hide_line.text = 'hide'

        else:
            hide_line.text = "Show"


        # if its start button have click this statment will run
        if (start):
            if (not game_thread.is_alive()):
                stop_threads = False
                game_thread = threading.Thread(target=main_game, args=(cell, lambda: stop_threads,), daemon=True)
                game_thread.start()

        # should draw the cells before red sqaure has drew >> as concept of layers
        writecells(screen, cell)

        if (hover(screen, posx, posy, small_cell)):
            if press == 1:
                cell = select_sq(cell, posx, posy, small_cell)
            elif press == 3:
                cell = clean_cell(cell, posx, posy,small_cell)

        txt = font.render("x = " + str(posx) + "y = " + str(posy), True, (255, 255, 255))
        screen.blit(txt, (x_crouser_text, y_crouser_text))
        screen.blit(size_text, (size_text_x, size_text_y))

        pg.display.update()


if __name__ == '__main__':
    main()
