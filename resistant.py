import pyglet.shapes

import vectors as vc
import person
import math
import random
from pyglet.gl import *
random.seed()

color_dict = {"red": (255,0,0), "green": (0,255,0), "blue": (0,0,255), "yellow": (255,255,0)}

persons = []

class MyWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(600,400)

def randomizer():
    if random.random()>0.5:
        if random.random()>0.5:
            x=62
            y=random.randint(62,height-62)
        else:
            x=62+rectangle2.x+rectangle2.width-5
            y=random.randint(62,height-62)
    else:
        if random.random() > 0.5:
            x = random.randint(62,width-62)
            y=62
        else:
            x = random.randint(62,width-62)
            y = rectangle2.y+rectangle2.height-5-3

    return x,y


def append_person(check):
    if check == 'create':
        persons.append(person.Person(x=random.randint(62,width-62),y=random.randint(62,height-62)))
        persons[len(persons)-1].rectangle = pyglet.shapes.Rectangle(persons[i].x, persons[i].y, 6,6, color=color_dict[persons[i].color], batch=batch)
        if random.random()<0.3:
            persons[len(persons) - 1].state.request1(persons[len(persons) - 1])
            if random.random()<0.5:
                persons[len(persons) - 1].state.request1(persons[len(persons) - 1])
    elif check == 'add':
        x,y = randomizer()
        persons.append(person.Person(x=x, y=y))
        if random.random() < 0.8:
            persons[len(persons)-1].state.request1(persons[len(persons)-1])
            persons[len(persons)-1].state.request1(persons[len(persons)-1])
            if random.random()<=0.4:
                persons[len(persons)-1].state.request1(persons[len(persons)-1])
                if random.random()<=0.5:
                    persons[len(persons)-1].state.request1(persons[len(persons) - 1])
                else:
                    persons[len(persons) - 1].state.request2(persons[len(persons) - 1])
        persons[len(persons)-1].rectangle = pyglet.shapes.Rectangle(persons[len(persons)-1].x, persons[len(persons)-1].y, 6,6, color=color_dict[persons[len(persons)-1].color], batch=batch)

def vector_creator():
    vector = vc.Vector2D(random.randint(-3, 3), random.randint(-3, 3))
    return vector

if __name__ == '__main__':
    height = 600
    width = 800
    window = MyWindow(width+120, height+100, "Simulation", resizable=True)
    batch = pyglet.graphics.Batch()
    rectangle = pyglet.shapes.BorderedRectangle(60, 60, width = width-120, height = height-120, border=5, border_color=(255, 22, 20), batch=batch)
    rectangle2 = pyglet.shapes.Rectangle(62,62, width-124, height-124, color=(0, 0, 0), batch=batch)
    for i in range(100):
        append_person('create')
        if random.random() < 0.8:
            persons[i].state.request2(persons[i])

    @window.event
    def moveT(dt):
        if random.random() <0.3:
            append_person('add')
        i=0
        while i<=len(persons)-1:
            if random.random()<=0.05:
                persons[i].vector = vector_creator()
            persons[i].x += persons[i].vector.get_components()[0]
            persons[i].y += persons[i].vector.get_components()[1]
            if persons[i].x <= rectangle2.x+rectangle2.width-5 and persons[i].x >= 62:
                if persons[i].y<=rectangle2.y+rectangle2.height-5-3 and persons[i].y >=62:
                    persons[i].rectangle = pyglet.shapes.Rectangle(x=persons[i].x, y=persons[i].y, width=6, height=6,
                                                           color=color_dict[persons[i].color], batch=batch)
                elif persons[i].rectangle is not None:
                    if random.random() >0.5:
                        persons[i].rectangle = persons[i].rectangle.delete()
                    else:
                        persons[i].vector = vc.Vector2D(x=-persons[i].vector.get_components()[0],
                                                        y=-persons[i].vector.get_components()[1])
            elif persons[i].rectangle is not None:
                persons[i].rectangle = persons[i].rectangle.delete()
                persons.pop(i)
            i+=1

        infected = []
        for i in range(len(persons)-1):
            if persons[i].color == "red" or persons[i].color == "yellow":
                if persons[i] not in infected:
                    infected.append(persons[i])
                for j in range(len(persons)-1):
                    if i !=j and persons[j].color == "green":
                        dist = math.sqrt((persons[i].x - persons[j].x)**2 + (persons[i].y - persons[j].y)**2)
                        if dist <30:
                            persons[j].last_time+=1
                            if persons[j].last_time==75:
                                if persons[i].color == "yellow":
                                    if random.random() <0.5:
                                        if random.random() < 0.5:
                                            persons[j].state.request1(persons[j])
                                        persons[j].state.request1(persons[j])
                                if persons[i].color == "red":
                                    if random.random() < 0.5:
                                        persons[j].state.request1(persons[j])
                                    persons[j].state.request1(persons[j])



        for i in range(len(infected)-1):
            infected[i].infection_time += 1
            if infected[i].infection_time==500:
                if infected[i].color == "yellow":
                    infected[i].state.request2(infected[i])
                    infected[i].state.request1(infected[i])
                if infected[i].color == "red":
                    infected[i].state.request1(infected[i])



    @window.event
    def on_draw():
        window.clear()
        batch.draw()

    pyglet.clock.schedule_interval(moveT, 1/25)
    pyglet.app.run()