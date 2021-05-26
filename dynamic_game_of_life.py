""""
Same previous Code but with dynamic programing implementation
Game of life by conway Is nice simple game have 4 rule.Imagine we play on bord have cells , every cell has two conditions live our die.
1: If a cell have 0  , 1   , 2 or more than 3 neighbor cells it will die
2: If a cell have have exactly 3 neighbor cells  will live

note : to remained myself : I used thread when I user click start button to run the main_game
Because it is my first project in pygamge : there are some bad implementation of pygame function and needless reusing it. I don't want to consume some time reediting it>
"""

import threading

try:
    import pygame as pg
except:
    import install_requirements
    import pygame as pg

import time
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox




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
        screen.blit(txt,(self.x + int(self.width / 2 - txt.get_width() / 2), self.y + int(self.length / 2 - txt.get_height() / 2)))
        
    # return True if the mouse hover over it
    def ishover(self, posx, posy):
        if (posx >= self.x and posx <= self.x + self.width and posy >= self.y and posy <= self.y + self.length):
            return True
        return False

    # return True if the button is clicked
    def isclicked(self, posx, posy):
        if (posx >= self.x and posx <= self.x + self.width and posy >= self.y and posy <= self.y + self.length):
            return True
        return False


# the cell have value of 0 if it is die and 1 if it is alive
class cells():
    def __init__(self, x=0, y=0, width=0):
        self.x = x
        self.y = y
        self.width = width
        self.value = 0
        self.img = pg.Surface((self.width, self.width))
        self.img.fill((61, 61, 61))

    # used this fucntion as subfunction for select_sq
    def fill(self):
        self.value = 1
        self.img.fill((113, 88, 226))

    def clean(self):
        self.value = 0
        self.img.fill((61, 61, 61))


class node():
    def __init__(self, valuey=None, valuex=None):
        self.next = None
        self.value = valuey, valuex


def image_pixel():
    global cell
    global w, h
    x = w
    y = h
    pixel = ""
    for i in range(y):
        for j in range(x):
            pixel = pixel + str(cell[i][j].value) + "," + str(i) + "," + str(j) + '\n'
    return pixel


# open file and save the excetince module
def save_module():
    root = tk.Tk()
    root.withdraw()
    try:
        file = filedialog.asksaveasfile(filetypes=[("Text file", "*.txt")], defaultextension=[("Text file", "*.txt")]).name
        array_str = image_pixel()
        save_txt = open(file, "w+")
        save_txt.write(array_str)
        save_txt.close()
    except Exception as ex:
        print(ex)
        tk.messagebox.showinfo(title="info", message="haven't saved ")
        return
    tk.messagebox.showinfo(title="info", message="Saved !!")


def open_module(screen):
    global w, h
    root = tk.Tk()
    root.wm_attributes('-topmost', 1)
    root.withdraw()
    file = filedialog.askopenfile(filetypes=[("Text file", "*.txt")], defaultextension=[("Text file", "*.txt")])
    wid, hi = w, h
    if(file==None):return
    y, x = select_place(screen)
    for line in file:
        try:
            pixel = list(map(int, line.split(',')))
        except:
            messagebox.showwarning(message="Wrong values!")
            return

        if (pixel[0] != 0 and pixel[0] != 1):
            messagebox.showwarning(message="Wrong values!")
            return

        if (pixel[1]+y >= hi or pixel[2]+x >= wid):
            continue
        if (pixel[0] == 0):
            remove_from_white_cell(pixel[1]+y, pixel[2]+x)
        else:
            append_to_white_cell(pixel[1]+y, pixel[2]+x)

def select_place(screen): # select the cell when I want to open the module
    global w
    small=True if w==114 or w==40 else False
    screen=pg.display.set_mode((screen.get_width(),screen.get_height()))
    while(True):
        screen.fill((75, 75, 75))
        posx,posy=pg.mouse.get_pos()
        writecells(screen)
        for event in pg.event.get():
            if event.type==pg.QUIT:
                pg.quit()
        press=pg.mouse.get_pressed()[0]
        if (posx < screen.get_width() - 112 and posy < screen.get_height() - 1):
            if not small:
                x = posx // 22
                xc=x
                x = x * 22
                y = posy // 22
                yc=y
                y = y * 22
                s = pg.Surface((20, 20))
                s.set_alpha(200)
                s.fill((46, 204, 113))
                screen.blit(s, (x + 2, y + 2))
                if press==1:
                 return yc,xc
            else:
                x = posx // 11
                xc=x
                x = x * 11
                y = posy // 11
                yc=y
                y = y * 11
                s = pg.Surface((10, 10))
                s.set_alpha(200)
                s.fill((46, 204, 113))
                screen.blit(s, (x + 1, y + 1))
                if press==1:
                 return yc,xc

        pg.display.update([0,0,screen.get_width()- 108,screen.get_height()])
# to check out if it is allow for the scan function to see the available cell >> to not cause a OUT OF RANGE error
def bondryx(j):
    global w
    return (j < w and j >= 0)


# same function but fro y axies
def bondryy(i):
    global  h
    return (i < h and i >= 0)


# this method is the core of the game, it is implement the rule mentioned before on the cell>
# it represents one generation of the game
def nib_count(y, x,cell):
    nib = 0
    dx = [-1, 0, 1, 1, 1, 0, -1, -1]
    dy = [-1, -1, -1, 0, 1, 1, 1, 0]
    i = 0
    while (i < 8):
        if (bondryx(dx[i] + x) and bondryy(dy[i] + y)  and cell[dy[i] + y][dx[i] + x] == 1):
            nib += 1
        i += 1
    return nib


def scan(cells,white_cell,stop):

    dx = [-1, 0, 1, 1, 1, 0, -1, -1]
    dy = [-1, -1, -1, 0, 1, 1, 1, 0]
    ref = [[cells[i][j].value for j in range(len(cells[0]))] for i in
           range(len(cells))]   # reference for the cell to compare with the first mode of the neighbor cell
    new_white=[]
    k=0
    limit=len(white_cell)
    while(k<limit):
        i,j = white_cell[k][0],white_cell[k][1]
        nib = nib_count(i, j,ref)
        if nib == 0 or nib == 1 or nib >= 4:
            cells[i][j].clean()
        else:
            new_white.append((i,j))
            cells[i][j].fill()

        for x in range(8):
            ya = i + dy[x]
            xa = j + dx[x]
            if (bondryx(xa) and bondryy(ya) and cells[ya][xa].value==0):
               nib = nib_count(ya, xa,ref)
               if nib == 3:
                    cells[ya][xa].fill()
                    new_white.append((ya,xa))


        k+=1
        if(stop()):
            break

    return cells,new_white


# main_game to continue play the game as far as there is an alive cell
def main_game(stop):
    global white_cell
    global cell
    sleep_t = 0.5
    while (len(white_cell)>0):
        cell,white_cell = scan(cell,white_cell,stop)
        time.sleep(sleep_t)

        if (stop()):  # this implementation used to pass a value to stop the thread
            break


def writecells(screen):  # draw the cells
    global cell
    global w, h
    x = w
    y = h
    for i in range(y):
        for j in range(x):
            screen.blit(cell[i][j].img, (cell[i][j].x, cell[i][j].y))


# iniat the cells in the begging of the game
# here ther is a bad implementation
# this fuction will iniat 20 * 20 cells if the window is small and 144* 64 if the window is large
def init_cells(large_screen, small):
    global cell
    global w,h
    x, y = 2, 2
    if (442 >= large_screen):
        if (small):
            w,h=40,40
            cell = [[cells() for _ in range(40)] for _ in range(40)]
            for i in range(40):
                x = 1
                for j in range(40):
                    cell[i][j] = cells(x, y, 10)
                    x = x + 11
                y = y + 11

        else:
            w,h=20,20
            cell = [[cells() for _ in range(20)] for _ in range(20)]
            for i in range(20):
                x = 2
                for j in range(20):
                    cell[i][j] = cells(x, y, 20)
                    x = x + 22
                y = y + 22

    else:
        if (small):
            w,h=114,64
            cell = [[cells() for _ in range(114)] for _ in range(64)]
            for i in range(64):
                x = 1
                for j in range(114):
                    cell[i][j] = cells(x, y, 10)
                    x = x + 11
                y = y + 11
        else:
            w,h=57,32
            cell = [[cells() for _ in range(57)] for _ in range(32)]
            for i in range(32):
                x = 2
                for j in range(57):
                    cell[i][j] = cells(x, y, 20)
                    x = x + 22
                y = y + 22


# draw a transparente red square when the crouser move around
def hover(screen, posx, posy, small):
    if (posx < screen.get_width() - 112 and posy < screen.get_height() - 1 and posx > 1 and posy>1):
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
def clean_cell(posx, posy, small):
    global cell
    global white_cell
    if small:
        x = posx // 11
        y = posy // 11
    else:
        x = posx // 22
        y = posy // 22

    remove_from_white_cell(y,x)


# blow the cell up and turn its value to 1
def select_sq(posx, posy, small):
    global cell
    global white_cell
    if small:
        x = posx // 11
        y = posy // 11
    else:
        x = posx // 22
        y = posy // 22
    append_to_white_cell(y,x)


# return all the value of the cells to 0
def clean_allcells():
    global cell
    global white_cell
    global w, h
    x = w
    y = h
    for i in range(y):
        for j in range(x):
            cell[i][j].clean()
    white_cell=[]

# backgound is created of the sqaure table
def drew_background(surface):
    global cell
    global w,h
    x = w
    y = h
    surface.fill((165, 177, 194))
    for i in range(y):
        for j in range(x):
            pg.draw.rect(surface, (0, 0, 0), [cell[i][j].x, cell[i][j].y, cell[i][j].width, cell[i][j].width], 0)

def append_to_white_cell(y,x):
    global white_cell
    global cell
    cell[y][x].fill()
    if((y,x) not in white_cell):
        white_cell.append((y,x))

def remove_from_white_cell(y,x):
    global white_cell
    global cell
    cell[y][x].clean()
    for i in range(len(white_cell)):
        if (y,x) == white_cell[i]:
            white_cell.pop(i)
            break
#global varible-----------------
w,h=0,0
cell = list(list())
white_cell = list()

#----------------------

# diplay the window
def main():
    global cell
    # display the window
    pg.init()
    screen = pg.display.set_mode((550, 442), pg.RESIZABLE)
    # initiate some variable
    small_cell = False
    font = pg.font.Font(pg.font.get_default_font(), 10)
    press = False  # to check if the the right mouse has clicked
    going = True  # stop while
    hide = True  # hide the background
    start = False  # start the main game
    size_text = font.render("cell size ", True, (255, 255, 255))  # give the user tow option for cells' size

    screen_width, screen_height = 550, 442
    screen = pg.display.set_mode((screen_width, screen_height), pg.RESIZABLE)
    init_cells(screen.get_height(), small_cell)
    background_cell = pg.Surface((screen.get_width() - 108, screen.get_height()))
    drew_background(background_cell)
    start_button = button(screen.get_width() - 100, screen.get_height() - 330, 90, 60, "start")
    hide_line = button(screen.get_width() - 100, screen.get_height() - 230, 90, 60, "Hide line")
    clean_button = button(screen.get_width() - 100, screen.get_height() - 130, 90, 60, "Clean")
    big_button = button(screen.get_width() - 50, screen.get_height() - 400, 45, 30, "Big")
    small_button = button(screen.get_width() - 100, screen.get_height() - 400, 45, 30, "small")
    open_button = button(screen.get_width() - 50, screen.get_height() - 365, 45, 30, 'open')
    save_button = button(screen.get_width() - 100, screen.get_height() - 365, 45, 30, 'Save')
    x_cursor_text = screen.get_width() - 100
    y_cursor_text = screen.get_height() - 40
    game_thread = threading.Thread(target=main_game, args=(lambda: stop_threads),daemon=True)
    size_text_x = screen.get_width() - 75
    size_text_y = screen.get_height() - 430
    
    while going:
        screen.fill((75, 75, 75))
        posx, posy = pg.mouse.get_pos()  # get the position of the mouse

        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False

            if event.type == pg.VIDEORESIZE:  # is work when the window is resized
                screen_width, screen_height = event.w, event.h
                screen = pg.display.set_mode((screen_width, screen_height), pg.RESIZABLE)
                init_cells(screen.get_height(), small_cell)
                background_cell = pg.Surface((screen.get_width() - 108, screen.get_height()))
                drew_background(background_cell)
                start_button = button(screen.get_width() - 100, screen.get_height() - 330, 90, 60, "start")
                hide_line = button(screen.get_width() - 100, screen.get_height() - 230, 90, 60, "Hide line")
                clean_button = button(screen.get_width() - 100, screen.get_height() - 130, 90, 60, "Clean")
                big_button = button(screen.get_width() - 50, screen.get_height() - 400, 45, 30, "Big")
                small_button = button(screen.get_width() - 100, screen.get_height() - 400, 45, 30, "small")
                open_button = button(screen.get_width() - 50, screen.get_height() - 365, 45, 30, 'open')
                save_button = button(screen.get_width() - 100, screen.get_height() - 365, 45, 30, 'Save')
                x_cursor_text = screen.get_width() - 100
                y_cursor_text = screen.get_height() - 40
                clean_allcells()
                size_text_x = screen.get_width() - 75
                size_text_y = screen.get_height() - 430

                game_thread = threading.Thread(target=main_game, args=(lambda: stop_threads),
                                               daemon=True)  # create thread of the main game and pass stop threads as varibale to control its functioninig
                stop_threads = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                press = event.button  # get the input value

                # check the buttons clicking
                if (press == 1 and small_button.isclicked(posx, posy)):
                    small_cell = True
                    init_cells(screen.get_height(), small_cell)
                    drew_background(background_cell)

                if (press == 1 and big_button.isclicked(posx, posy)):
                    small_cell = False
                    init_cells(screen.get_height(), small_cell)
                    drew_background(background_cell)

                if (press == 1 and hide_line.isclicked(posx, posy)):
                    hide = False if (hide) else True

                if (press == 1 and start_button.isclicked(posx, posy)):
                    if start:
                        start = False
                        start_button.text = "Run"
                        stop_threads = True
                    else:
                        stop_threads = False
                        start = True
                        start_button.text = "Stop"

                if (press == 1 and clean_button.isclicked(posx, posy)):
                    clean_allcells()
                    start = False
                    start_button.text = "Run"
                    stop_threads = True

                if (press == 1 and open_button.isclicked(posx, posy)):
                    open_module(screen)
                    screen = pg.display.set_mode((screen_width, screen_height), pg.RESIZABLE)
                if (press == 1 and save_button.isclicked(posx, posy)):

                    save_module()

            elif event.type == pg.MOUSEBUTTONUP:
                press = 0

        # draw the buttons
        clean_button.draw_button(screen, posx, posy)
        hide_line.draw_button(screen, posx, posy)
        start_button.draw_button(screen, posx, posy)
        big_button.draw_button(screen, posx, posy)
        small_button.draw_button(screen, posx, posy)
        save_button.draw_button(screen, posx, posy)
        open_button.draw_button(screen, posx, posy)
        # space_button.draw_button(screen,posx,posy)
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
                game_thread = threading.Thread(target=main_game, args=(lambda: stop_threads,), daemon=True)
                game_thread.start()

        # should draw the cells before red sqaure has drew >> as concept of layers
        writecells(screen)

        if (hover(screen, posx, posy, small_cell)):
            if press == 1:
                select_sq(posx, posy, small_cell)
            elif press == 3:
                clean_cell(posx, posy, small_cell)

        txt = font.render("x = " + str(posx) + "y = " + str(posy), True, (255, 255, 255))
        screen.blit(txt, (x_cursor_text, y_cursor_text))
        screen.blit(size_text, (size_text_x, size_text_y))

        pg.display.update()


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print('error' ,ex)

    