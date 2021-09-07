"""
Copyright 2020 Patrick Müller
Tetris
"""
from Gamelogic import *
from Graphic import *

# make big while loop and then some smaller for the different menues and a state variable to switch in between
state = 0
game = GameLogic()
g = Graphic(game, state)
g.root.bind("<Up>", g.event_handler)  # call function that calls the movement func first then update canvas
g.root.bind("x", g.event_handler)
g.root.bind("<Right>", g.event_handler)
g.root.bind("<Left>", g.event_handler)
g.root.bind("<Escape>", g.event_handler)
while g.state != -1:
    while g.state == 0:
        # start menu
        g.state = 1

    if g.state == 1:
        g.init_canvas()
        g.update_canvas()
        g.next_tetrimino()
        g.score_co(4, 3, 0)
        g.root.bind("<Up>", g.event_handler) 
        g.root.bind("x", g.event_handler)
        g.root.bind("<Right>", g.event_handler)
        g.root.bind("<Left>", g.event_handler)
        g.root.bind("<Escape>", g.event_handler)
    while g.state == 1:
        g.update_canvas()
        g.root.update_idletasks()
        g.root.update()
        time.sleep(0.3)
        if game.move_down() is False:
            game.spawn_tetrimino()
        if game.is_lost():
            break
        g.update_canvas()
        g.root.update_idletasks()
        g.root.update()

    while g.state == 2:
        # pause menu
        g.root.update_idletasks()
        g.root.update()