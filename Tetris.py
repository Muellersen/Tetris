"""
Copyright 2020 Patrick Müller
Tetris
"""
from Gamelogic import *
from Graphic import *
from time import time

# make big while loop and then some smaller for the different menues and a state variable to switch in between
state = 0
previous_state = 0
game = GameLogic()
g = Graphic(game, state)

while g.state != -1:
    while g.state == 0:
        # start menu
        previous_state = 0
        g.state = 1

    if g.state == 1 and previous_state == 0:
        g.init_canvas()
        g.update_canvas()
        g.next_tetrimino()
        g.init_score()
        g.root.bind("<Up>", g.event_handler) 
        g.root.bind("x", g.event_handler)
        g.root.bind("<Right>", g.event_handler)
        g.root.bind("<Left>", g.event_handler)
        g.root.bind("<Down>", g.event_handler)
        g.root.bind("<space>", g.event_handler)
        g.root.bind("<Escape>", g.event_handler)
        previous_state = 1
    while g.state == 1:
        # game active
        # while loop for player control and delay
        timeout = time() + (0.8 - (game.level - 1) * 0.007)**(game.level - 1)
        while True:
            g.update_canvas()
            g.update_score()
            g.root.update_idletasks()
            g.root.update()
            if time() > timeout:
                break

        if game.move_down() is False:
            game.spawn_tetrimino()
        game.line_is_full()

        if game.is_lost():
            g.state = -1
            break
        g.update_canvas()
        g.update_score()
        g.root.update_idletasks()
        g.root.update()

    while g.state == 2:
        # pause menu
        g.root.update_idletasks()
        g.root.update()
