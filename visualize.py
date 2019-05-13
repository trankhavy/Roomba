import turtle
from turtle import *
from classes import SetUp, Roomba
import time

def draw_box(t,x,y,size,fill_color):
    t.penup() # no drawing!
    t.goto(x,y) # move the pen to a different position
    t.pendown() # resume drawing

    t.fillcolor(fill_color)
    t.begin_fill()  # Shape drawn after this will be filled with this color!

    for i in range(0,4):
        t.forward(size) # move forward
        t.right(90) # turn pen right 90 degrees

    t.end_fill() # fill the rectangle

def draw_room(r,start_x,start_y,board,box_size):
    room = r.layout
    nx = r.room.nx
    ny = r.room.ny
    for i in range(0,nx):
        for j in range(0,ny):
            square_color = 'grey' if room[i,j] == 2 else 'white' # toggle after a column
            draw_box(board,start_x+j*box_size,start_y+i*box_size,box_size,square_color)

def visualize(r,strategy,box_size=30,steps=1000):
    wn = Screen()
    board = turtle.Turtle()
    board.hideturtle()
    board.speed(0)
    turtle.penup()
    turtle.goto(-100,100)
    turtle.pendown()
    turtle.write(strategy,font=("Time News Roman",16,"bold"))

    nx = r.room.nx
    ny = r.room.ny
    start_x = -200 # starting x position of the floor
    start_y = -200 # starting y position of the floor
    draw_room(r,start_x,start_y,board,box_size)
    # Go to roomba starting place
    turtle.penup()
    middle_start_x = start_x+r.x_start*box_size + box_size/2
    middle_start_y = start_y+r.y_start*box_size - box_size/2
    turtle.goto(middle_start_x,middle_start_y)
    if strategy == "random_walk":
        x,y = r.random_step()[0]
        x_coor = start_x+y*box_size + box_size/2
        y_coor = start_y+x*box_size - box_size/2
        turtle.goto(x_coor,y_coor)
    else:
        r.layout[0,0] = 0
        r.x_start = 0
        r.y_start = 0
        r.current_x = 0
        r.ccurent_y = 0
        r.move_to(r.x_start,r.y_start)
        x_coor = start_x+r.x_start*box_size + box_size/2
        y_coor = start_y+r.y_start*box_size - box_size/2
        turtle.goto(x_coor,y_coor)

    turtle.pendown()

    turtle.pencolor('green')
    board.showturtle()
    for i in range(steps):
        # If all the tile is clean, stop the simulation
        if r.check_clean() == True:
            break
        else:
            # Calculate step using other strategy
            step = r.step(strategy)
            print(step)
            for i in range(len(step)):
                x = step[i][0]
                y = step[i][1]
                r.move_to(x,y)
                x_coor = start_x+y*box_size + box_size/2
                y_coor = start_y+x*box_size - box_size/2
                turtle.goto(x_coor,y_coor)



    board.speed(1)
    turtle.mainloop()
