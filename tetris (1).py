
import pygame, sys, random
import math
import numpy as np

pygame.init()


width = 400
height = 800

screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
red_square = pygame.Surface((20,20))
red_square.fill(pygame.Color("red"))
blue_square = pygame.Surface((20,20))
blue_square.fill(pygame.Color("blue"))
yellow_square = pygame.Surface((20,20))
yellow_square.fill(pygame.Color("yellow"))
white_square = pygame.Surface((20,20))
white_square.fill(pygame.Color("white"))


x_init = 25
y_init = 0
x = 0
y = 0
#function global variables
counter = 0
speed = 10
add = 1
score = 0

#blocks and their shapes
square_block = [(0,7),(0,8),(1,7),(1,8)]
line_block = [(0,7),(0,8),(0,9),(0,10)]
pyramid_block = [(0,8),(1,7),(1,8),(1,9)]
zigzag_right_block = [(0,7),(0,8),(1,8),(1,9)]
zigzag_left_block = [(0,9),(0,8),(1,8),(1,7)]
L_left_block = [(0,7),(1,7),(1,8),(1,9)]
L_right_block = [(1,7),(1,8),(1,9),(0,9)]
blocks = [square_block, line_block, pyramid_block, zigzag_right_block, zigzag_left_block, L_left_block,L_right_block]
#blocks = [line_block]
colors = [-1,-2,-3]

M_r = 30
M_c = 16

#seeting up the canvas
M = np.zeros((M_r,M_c)) 
wall = []
for _ in range(30):
    wall.append(10)
floor = []
for _ in range (16):
    floor.append(10)
M[:,0] = wall
M[:,-1] = wall
M[-1,:] = floor

next = np.zeros((4,4))


def update_canvas(M):
    for index,value in np.ndenumerate(M):
        if abs(value) == 3:
            x = x_init + index[1]*22 
            y = y_init + index[0]*22 
            screen.blit(yellow_square,(x,y))
        if abs(value) == 2:
            x = x_init + index[1]*22 
            y = y_init + index[0]*22 
            screen.blit(red_square,(x,y))
        if abs(value) == 1:
            x = x_init + index[1]*22
            y = y_init + index[0]*22 
            screen.blit(blue_square,(x,y))
        if abs(value) == 10:
            x = x_init + index[1]*22
            y = y_init + index[0]*22 
            screen.blit(white_square,(x,y))

def block_movement_down(M):
    
    block_pos = []
    block_color = 0
    move = True
    global counter
    
    if speed == 1 and counter > 10:
        counter = 0 
    if counter == speed:
        for index,value in np.ndenumerate(M):
            if value < 0:
                block_pos.append(index)
                block_color = value

        for i in block_pos: 
            if i[0]+1 > M_r-1  or M[i[0]+1, i[1]] > 0:   
                move = False
        if not move:
            for i in block_pos:
                if M[i] == -1:
                    M[i] = 1
                if M[i] == -2:
                    M[i] = 2
                if M[i] == -3:
                    M[i] = 3         
        if move == True:
            for i in block_pos:
                M[i] = 0
            for i in block_pos: 
                M[i[0]+1, i[1]] = block_color
        counter = 0 
    else:
        counter += 1

def block_movement_horizontal(M,direc):
    block_pos = []
    block_color = 0
    move = True
    for index,value in np.ndenumerate(M):
        if value < 0:
            block_pos.append(index)
            block_color = value
    for i in block_pos:   
        if i[1]+direc < 1 or i[1]+direc > M_c-2 or M[i[0],i[1]+direc] > 0:
            move = False
    if move == True:
        if direc == -1:
            for i in block_pos:
                M[i] = 0
            for i in block_pos: 
                M[i[0], i[1]-1] = block_color
        elif direc == 1:
            for i in block_pos:
                M[i] = 0
            for i in block_pos: 
                M[i[0], i[1]+1] = block_color
 
def spawn_block(M):
    if M.min() >= 0: 
        global add
        add = 1
        block = random.choice(blocks)
        color = random.choice(colors)
        for i in block:
            M[i] = color

def check_line(M):
    lines = []
    for i in range(M_r-1):
        line = True
        for j in range(M_c-1):
            if M[i][j] <= 0:
                line = False
        if line == True:
            lines.append(i)
            global score
            score += 1  
            print(score)     
    return lines

def clear_line(M,lines):
    clear_line = [10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10]  
    M = np.delete(M, lines, axis=0)
    M =  np.vstack([np.tile(clear_line, (len(lines), 1)), M])     
    return M

def identify_bounding_box():
    
    rows,columns = np.where(M < 0)
    size = max(len(np.unique(rows)),len(np.unique(columns))) 
    global add  
    if size == 3:
        if add == 1:
            return min(rows), min(rows)+size-1 , min(columns), min(columns)+size-1, size   
        if add == 2:
            return min(rows), min(rows)+size-1 , min(columns)-1, min(columns)+size-2, size
        if add == 3:
            return min(rows)-1, min(rows)+size-2, min(columns), min(columns)+size-1, size   
        if add == 4:
            return min(rows), min(rows)+size-1 , min(columns), min(columns)+size-1, size              
    elif size == 4:
        if add == 1:
            return min(rows)-1, min(rows)+size-2 , min(columns), min(columns)+size-1, size   
        if add == 2:
            return min(rows), min(rows)+size-1 , min(columns)-2, min(columns)+size-3, size
        if add == 3:
            return min(rows)-2, min(rows)+size-3, min(columns), min(columns)+size-1, size   
        if add == 4:
            return min(rows), min(rows)+size-1 , min(columns)-1, min(columns)+size-2, size 
    else:
            return min(rows), min(rows)+size-1 , min(columns), min(columns)+size-1, size 
         
def rotation(M):
    row0, row1, column0, column1, size = identify_bounding_box()
    M2 = M.copy()
    rot = True
    if size == 3 and len(M[row0:row1+1,column0:column1+1][1]) == 3 or size == 4 and len(M[row0:row1+1,column0:column1+1][1]) == 4 and len(M[row0:row1+1,column0:column1+1][0]) == 4:
        for i in np.arange(row0,row1+1): 
            for j in np.arange(column0,column1+1):
                if M[i,j] <= 0:
                    M2[j-column0 + row0, column1 - i + row0] = M[i,j]  
            
        for index,value in np.ndenumerate(M):
            if value > 0:
                if M2[index] != value:
                    rot = False
    global add 
    if rot == False:
        M2 = M
    elif rot == True:
        if add != 4:
            add += 1
        else:
            add = 1               
    return M2
               
while True:
   
    for event in pygame.event.get():
        direc = 0
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_LEFT:
                direc = -1
                block_movement_horizontal(M,direc)
            if event.key == pygame.K_RIGHT:                
                direc = 1
                block_movement_horizontal(M,direc)
            if event.key == pygame.K_UP:                
                M = rotation(M)                   
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        speed = 1    
    else:
        speed = 10
    screen.fill("black")
    spawn_block(M)
    block_movement_down(M) 
    lines = check_line(M)
    if len(lines) > 0:
        M = clear_line(M,lines)          
    update_canvas(M)
    pygame.display.update()
    clock.tick(60)
    





