import turtle
import random
from threading import Thread


def move(x, y):
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()


def draw_virus(x, y):
    move(x, y)
    for i in range(1, 200):
        turtle.forward(i)
        turtle.left(i)


if __name__ == '__main__':
    turtle.screensize(1920, 1080, "black")
    turtle.shape("turtle")  # 设置画笔的形状
    turtle.pencolor('green')  # 设置画笔的颜色
    thread_list = []
    for _ in range(10):
        coordinate_x = random.randint(-800, 800)
        coordinate_y = random.randint(-300, 300)
        th1 = Thread(target=draw_virus, args=(coordinate_x, coordinate_y,))
        thread_list.append(th1)
    #
    # for th in thread_list:
    #     print(th)

    for th in thread_list:
        th.start()

    for th in thread_list:
        th.join()

    turtle.mainloop()
