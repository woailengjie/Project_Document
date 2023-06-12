import turtle
import random
from threading import Thread

COLOR = ['red', 'orange', 'yellow', 'green', 'limegreen', 'blue', 'purple']


def move(p, x, y):
    p.penup()
    p.goto(x, y)
    p.pendown()


def draw_virus(pen, x, y, pen_color):
    pen.pencolor(pen_color)  # 设置画笔的颜色
    move(pen, x, y)
    line = random.uniform(0.6, 1.5)
    for i in range(1, 200):
        pen.forward(line * i)
        pen.left(i)


if __name__ == '__main__':
    screen = turtle.getscreen()
    screen.screensize(1920, 1080, "black")
    thread_list = []

    for i in range(7):
        pen = turtle.Turtle()
        pen.shape("turtle")  # 设置画笔的形状
        pen.speed(0)        # 设置画笔的速度
        coordinate_x, coordinate_y = random.randint(-400, 400), random.randint(-300, 300)
        th1 = Thread(target=draw_virus, args=(pen, coordinate_x, coordinate_y, COLOR[i],))
        thread_list.append(th1)

    for th in thread_list:
        th.start()
    screen.mainloop()