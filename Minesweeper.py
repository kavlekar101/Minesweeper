import pygame
import random
from Tkinter import*
import os
import numpy
import math

IMGS = [pygame.transform.scale(pygame.image.load(os.path.join("Games/Pics","1.jpeg")),(40,40)),
        pygame.transform.scale(pygame.image.load(os.path.join("Games/Pics","2.jpeg")),(40,40)),
        pygame.transform.scale(pygame.image.load(os.path.join("Games/Pics","3.jpeg")),(40,40)),
        pygame.transform.scale(pygame.image.load(os.path.join("Games/Pics","4.jpeg")),(40,40)),
        pygame.transform.scale(pygame.image.load(os.path.join("Games/Pics","5.jpeg")),(40,40)),
        pygame.transform.scale(pygame.image.load(os.path.join("Games/Pics","6.jpeg")),(40,40)),
        pygame.transform.scale(pygame.image.load(os.path.join("Games/Pics","7.jpeg")),(40,40)),
        pygame.transform.scale(pygame.image.load(os.path.join("Games/Pics","8.jpeg")),(40,40)),
        pygame.transform.scale(pygame.image.load(os.path.join("Games/Pics","flag.jpeg")),(40,40)),
        pygame.transform.scale(pygame.image.load(os.path.join("Games/Pics","mine.jpeg")),(40,40))]

#just a regular block
class Block(object):
    #change to false before you play the actual game
    #multiply all of the x and y by 40
    def __init__(self,x,y,num,type,uncovered=False,flag=False):
        self.x = x
        self.y = y
        self.uncovered = uncovered
        self.num = num
        self.type = type
        self.flag = flag

    def draw(self,screen):
        if not(self.uncovered):
            pygame.draw.rect(screen,(0,0,0),[self.x*40,self.y*40,40,40])
            if(self.flag):
                screen.blit(IMGS[8],(self.x*40,self.y*40))
        else:
            if(self.num-1>=0):
                screen.blit(IMGS[self.num-1],(self.x*40,self.y*40))
#creates a mine
class Mine(Block):
    def __init(self,x,y,num,type,uncovered,flag):
        super.__init__(x,y,num,type,uncovered,flag)
        #don't really need this
        self.num = -1000
        self.type = type
        self.flag = flag

    def draw(self,screen):
        won = True
        restart = False
        if not(self.uncovered):
            pygame.draw.rect(screen,(0,0,0),[self.x*40,self.y*40,40,40])
            if(self.flag):
                screen.blit(IMGS[8],(self.x*40,self.y*40))
            if(board.nums == 10):
                for i in range(len(board.mines)):
                    numbers = board.mines[i].split(",")
                    x1,y1 = int(numbers[0]),int(numbers[1])
                    if(board.arr[x1][y1].uncovered):
                        won = False
                if won:
                    restart = True
                    print("Congrats, you won!")

        else:
            screen.blit(IMGS[9],(self.x*40,self.y*40))
            if(self.num == -1000):
                for i in range(len(board.arr)):
                    for j in range(len(board.arr[i])):
                        board.arr[j][i].uncovered = True


            self.num = -2000
            restart = True
            print("Congrats, you lost!")
    def is_mine(self):
        return self.mine

#keeps track of the board
class Board():
    def __init__(self,rows,cols,nums=100):
        self.rows = rows
        self.cols = cols
        self.mines = []
        self.arr = [[Block(j,i,0,"block") for i in range(cols)] for j in range(rows)]
        self.nums = nums

    def events(self,screen):
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif(event.type == pygame.MOUSEBUTTONUP):
                    pos = pygame.mouse.get_pos()
                    x,y = pos[0]/40,pos[1]/40
                    if(event.button == 1):
                        if(len(self.mines) == 0):
                            self.arr[x][y].uncovered = True
                            self.arr[x][y].draw(screen)
                            differ_rands(x,y)
                        self.uncover(x,y)
                    elif(event.button == 2):
                        os.execl(sys.executable,sys.executable,*sys.argv)
                    elif(event.button == 3):
                        self.arr[x][y].flag = not(self.arr[x][y].flag)

        except pygame.error as p:
            pass

    def uncover(self,x,y):
        if not(self.arr[x][y].flag):
            self.arr[x][y].uncovered = True
            self.nums -= 1
        if(self.arr[x][y].num > 0 or self.arr[x][y].type == "mine"):
            return
        elif(self.arr[x][y].num == 0):
            surroundings = find_surroundings(x,y)
            for i in range(len(surroundings)):
                if(i%2!=0):
                    continue
                x1,y1 = surroundings[i],surroundings[i+1]
                if(self.arr[x1][y1].type == "block"):
                    if(not(self.arr[x1][y1].uncovered)):
                            self.uncover(x1,y1)


#returns list of surrounding blocks
def find_surroundings(x,y):
    surroundings = []
    for i in range(8):
        theta = math.pi+(math.pi/4*i)
        xdiff,ydiff = math.cos(theta),math.sin(theta)
        if(i%2 != 0):
            xdiff *= math.sqrt(2)
            ydiff *= math.sqrt(2)
        x1,y1 = x+int(round(xdiff)),y+int(round(ydiff))
        if(x1<0 or y1<0 or x1>len(board.arr)-1 or y1>len(board.arr[0])-1):
            continue
        surroundings.append(x1)
        surroundings.append(y1)
    return surroundings

#finds random places for the mines and sets them there
def differ_rands(x,y):
    randx,randy = [],[]
    surroundings = []
    mines = 20

    for i in range(8):
        theta = math.pi+(math.pi/4*i)
        xdiff,ydiff = math.cos(theta),math.sin(theta)
        if(i%2 != 0):
            xdiff *= math.sqrt(2)
            ydiff *= math.sqrt(2)
        x1,y1 = x+int(round(xdiff)),y+int(round(ydiff))
        surroundings.append(str(x1)+","+str(y1))

    while(len(randx) == 0):
        for i in range(mines):
            randx.append(random.randint(0,board.rows-1))
            randy.append(random.randint(0,board.cols-1))
        should = False
        for i in range(mines):
            for j in range(mines):
                if(i == j):
                    continue
                elif((randx[i] == randx[j] and randy[i] == randy[j])
                        or (randx[i] == x and randy[i] == y)):
                    should = True
                else:
                    for k in range(len(surroundings)):
                        numbers = surroundings[k].split(",")
                        x1,y1 = int(numbers[0]),int(numbers[1])
                        if(randx[i] == x1 and randy[i] == y1):
                            should = True
        if should:
            randx,randy = [],[]


    for i in range(len(randx)):
        board.mines.append(str(randx[i])+","+str(randy[i]))
        board.arr[randx[i]][randy[i]] = Mine(randx[i],randy[i],-1000,"mine")

    for i in range(len(board.mines)):
        string = board.mines[i].split(",")
        set_nums(i,int(string[0]),int(string[1]))

#sets the number tiles
def set_nums(num,x,y):
    surroundings = find_surroundings(x,y)
    for i in range(len(surroundings)):
        if(i%2!=0):
            continue
        x1,y1 = surroundings[i],surroundings[i+1]
        if(board.arr[x1][y1].type == "block"):
            board.arr[x1][y1].num += 1

#creates window
def create_window(screen):
    try:
        screen.fill((127,127,127))
        for row in board.arr:
            for piece in row:
                piece.draw(screen)
        for i in range(11):
            pygame.draw.line(screen,(110,110,110),(0,0+i*40),(401,0+40*i))
            pygame.draw.line(screen,(110,110,110),(0+i*40,0),(0+40*i,401))

        pygame.display.update()
    except pygame.error as p:
        pass
def main():
    global board
    pygame.init()
    running = True
    cols = 10
    rows = 10
    board = Board(rows,cols)
    screen = pygame.display.set_mode((cols*40,rows*40))
    while running:
        create_window(screen)
        board.events(screen)

main()
