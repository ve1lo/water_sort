from tkinter import *
from turtle import color
from types import new_class
import numpy as np
import random

mainx = 50
mainy = 50
maincanvasizex = 600
maincanvasizey = 650


root = Tk() 
c = Canvas(root, width=maincanvasizex, height=maincanvasizey, bg='white')
c.pack()

# def menu():
#     c.delete('all')
#     c.create_rectangle(0,0,600,600,fill='grey', tags='menubg')
#     c.create_rectangle(150,250,450,300,fill='white', tags='startbutton')
#     c.create_text(300,275,text='Generate level', font='Verdana 18', anchor='center', tags='startbutton')    
#     c.tag_bind('startbutton','<Button-1>',startgame)

dict_digits = {
    0:{'color_block':'gray'},
    1:{'color_block':'#ff0000'},
    2:{'color_block':'#6495ED'},
    3:{'color_block':'#006400'},
    4:{'color_block':'#98FB98'},
    5:{'color_block':'#FFD700'},
    6:{'color_block':'#FF69B4'},
    7:{'color_block':'#EEAEEE'},
    8:{'color_block':'#ff0ff0'},
    9:{'color_block':'#ff00ff'},
    10:{'color_block':'#006400'},
    11:{'color_block':'#98FB98'},
    12:{'color_block':'#FFD700'},
    13:{'color_block':'#FF69B4'},
    14:{'color_block':'#EEAEEE'},
    15:{'color_block':'#ff0ff0'},
    16:{'color_block':'#ff00ff'},  
}




count_colors=4
pole = np.zeros((count_colors,4), dtype=int)
count_empty_colbs = 2
cells = count_colors*4
count_colbs = count_colors + count_empty_colbs

# b = [[1,1,1,1]]
# pole = np.concatenate((pole,b),axis=0)


def start_fill_pole():
    for i in range(count_colors):
        while np.count_nonzero(pole==i+1) < 4:
            x = random.randint(0,count_colors-1)
            y = random.randint(0,3)
            d = i+1
            if pole[x][y] == 0:
                pole[x][y] = d
    add_empty_colbs()
    render()

def add_empty_colbs():
    global pole
    a = [[0,0,0,0]]
    for i in range(count_empty_colbs):
        pole = np.concatenate((pole,a),axis=0)
    

def render():
    gap = 0
    j = 0
    for i in range(count_colbs):
        if i % 6==0:
            gap += 150
            j = 0
        for colba in range(4):
            c.create_rectangle(mainx+60*(j+1),gap+colba*25,mainx+30+60*(j+1),25+gap+colba*25, fill=dict_digits[pole[i][colba]]['color_block'], tags = 'water')
        j+=1
    #print(pole)
    c.tag_bind('water','<Button-1>',select_colba)
    win_or_not()
        



def startgame():
    c.delete('all')
    c.create_rectangle(0,0,maincanvasizex,maincanvasizey,fill='grey', tags='menubg')
    gap = 0
    j = 0
    for i in range(count_colbs):    
        if i % 6==0:
            gap += 150
            j = 0
        c.create_rectangle(mainx+60*(j+1),gap,mainx+30+60*(j+1),100+gap, tags = 'colba')
        j +=1
    c.tag_bind('colba','<Button-1>',select_colba)
    c.tag_bind('menubg','<Button-1>',deselect_colba)    



selected_colba = -1
ifselected = 0

def select_colba(event):
    global selected_colba
    global ifselected
    if selected_colba < 0:
        selected_colba = -1        
    posx = event.x
    posy = event.y
    row = posy // 150
    col = (posx - mainx)//60
    colba_num = col + 5*row - 5
    if ifselected == 0: 
        c.create_rectangle(mainx+60*(col),row*150,mainx+30+60*(col),100+row*150, tags = 'select_colb', width=2, outline='#000000')
        ifselected = 1
        selected_colba = colba_num
    else:
        deselect_colba(event) 
    if (selected_colba != colba_num) and (ifselected == 0):
        #главная механика переливания
        take_water(selected_colba, colba_num)


def delete_zero_from_colba(a):
    c = []
    for i in range(4):
        c.append(a[i])
    print(c)
    i = 0
    while i<4:
        if c[i]==0:
            c.remove(0)
            i -=1
        else:
            break
        i+=1
    return(c)

def get_oldwater(c):
    i = 0
    print('получаем')
    oldwater = []
    oldwater.append(c[0])
    for i in range(1,len(c)):
        if oldwater[0] == c[i]:
            oldwater.append(c[i])
        else:
            break
    print(oldwater)
    return oldwater

def take_water(selected_colba, colba_num):
    print('перелив')
    oldcolba = pole[selected_colba-1]
    newcolba = pole[colba_num-1]
    no_zero_old_colba = delete_zero_from_colba(oldcolba)
    if oldcolba[0]==oldcolba[1] and oldcolba[2] == oldcolba[3] and oldcolba[0] == oldcolba[2]:
        oldwater=[oldcolba[0],oldcolba[0],oldcolba[0],oldcolba[0]]
    else:
        if np.array_equal(oldcolba,[0,0,0,0]):
            pass
        else:
            oldwater = get_oldwater(no_zero_old_colba)
    print('oldcolba')
    print(oldcolba)
    put_water(oldwater, newcolba, oldcolba)
    
def delete_water_from_oldcolba(oldcolba, oldwater):
    count_empty_water = 0
    for i in oldcolba:
        if i == 0:
            count_empty_water +=1
    for i in range(len(oldwater)):
        oldcolba[count_empty_water+i] = 0

def put_water(oldwater, newcolba, oldcolba):
    count_empty_water = 0
    for i in newcolba:
        if i==0:
            count_empty_water +=1
    color_test = 0
    for i in newcolba:
        if i != 0:
            color_test = i
            break
    if len(oldwater) > 0:
        if len(oldwater)<=count_empty_water:
            if oldwater[0] == color_test or color_test==0:
                for i in range(len(oldwater)):
                    newcolba[count_empty_water-i-1] = oldwater[i]
                delete_water_from_oldcolba(oldcolba, oldwater)
    else:
        print(oldwater)
    print()
    print(newcolba)
    render()
   
def deselect_colba(event):
    global ifselected
    c.delete('select_colb')
    ifselected = 0 

def win_or_not():
    wincolb = 0
    for i in range(count_colbs):
        if pole[i][0]==pole[i][1] and pole[i][1] == pole[i][2] and pole[i][0] == pole[i][2]:
            wincolb += 1
    if count_colbs == wincolb:
        print('WIN')
        return True
    else:
        print('Still play')
        return False

startgame()
start_fill_pole()

root.mainloop()