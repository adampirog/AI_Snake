import pygame
from scipy.spatial import distance
import random

WIDTH = 600
HEIGHT = 600

SIDE = 15

VEL = 4


def collision(cube1, cube2, tollerance=0):

    en = (cube1.x, cube1.y)
    ms = (cube2.x, cube2.y)

    dist = distance.euclidean(en, ms)

    if(dist <= tollerance):
        return True
    return False


class Cube:
    
    def __init__(self, x, y, x_move, y_move, color=(255, 0, 0)):
        self.x = x
        self.y = y
        self.color = color
        self.x_move = x_move
        self.y_move = y_move
        
        self.movX = 0
        self.movY = 0
        
        self.isLast = True
        
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, SIDE, SIDE)) 
    
    def update_position(self):
        global HEIGHT, WIDTH

        self.x += self.x_move
        self.y += self.y_move       

        if(self.x < 0):
            self.x = WIDTH
        elif(self.x > WIDTH):
            self.x = 0
        
        if(self.y < 0):
            self.y = HEIGHT
        elif(self.y > HEIGHT):
            self.y = 0
              
    def move(self, x_move, y_move):
        self.x_move = x_move
        self.y_move = y_move
        
            
class Snake():
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_move = 0
        self.y_move = 0
        
        self.body = [Cube(x, y, 0, 0)]
        self.turns = []
        self.snacks = []
        
        self.spawn_snack()
            
    def spawn_snack(self):
        self.snacks.append(Snack(random.randint(0, WIDTH - 50), random.randint(0, HEIGHT - 50)))
    
    def right(self):
        self.x_move = VEL
        self.y_move = 0
        self.turns.append(Turn(self.x, self.y, self.x_move, self.y_move))
        
    def left(self):
        self.x_move = -VEL
        self.y_move = 0
        self.turns.append(Turn(self.x, self.y, self.x_move, self.y_move))
        
    def up(self):
        self.x_move = 0
        self.y_move = -VEL
        self.turns.append(Turn(self.x, self.y, self.x_move, self.y_move))
    
    def down(self):
        self.x_move = 0
        self.y_move = VEL
        self.turns.append(Turn(self.x, self.y, self.x_move, self.y_move))
        
    def update_position(self, window):
        
        self.x += self.x_move
        self.y += self.y_move
        
        # snack eating
        #for snack in list(self.snacks):
            #snack.draw(window)
            #if(collision(self, snack, 15)):
                #self.snacks.remove(snack)
                #self.add_cube()
                #self.spawn_snack()
        
        for cube in self.body:
            cube.update_position()
            cube.draw(window)

            for turn in list(self.turns):
                if collision(turn, cube):
                    cube.move(turn.x_move, turn.y_move)
                    if(cube.isLast):
                        self.turns.remove(turn)

        if(self.x < 0):
            self.x = WIDTH
            self.add_cube()
        elif(self.x > WIDTH):
            self.x = 0

        if(self.y < 0):
            self.y = HEIGHT
        elif(self.y > HEIGHT):
            self.y = 0
            
    def move(self, window):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.left()

        if keys[pygame.K_RIGHT]:
            self.right()
            
        if keys[pygame.K_UP]:
            self.up()
            
        if keys[pygame.K_DOWN]:
            self.down()

        self.update_position(window)

    def add_cube(self):
        
        tail = self.body[-1]
        
        if(tail.x_move == 0):
            if(tail.y_move > 0):
                self.body.append(Cube(tail.x, (tail.y) - SIDE - 2, tail.x_move, tail.y_move))     
            else:
                self.body.append(Cube(tail.x, (tail.y) + SIDE + 2, tail.x_move, tail.y_move))  

        elif(tail.y_move == 0):
            if(tail.x_move > 0):
                self.body.append(Cube((tail.x) - SIDE - 2, tail.y, tail.x_move, tail.y_move))
            else:
                self.body.append(Cube((tail.x) + SIDE + 2, tail.y, tail.x_move, tail.y_move))
                
        tail.isLast = False


class Turn:
    def __init__(self, x, y, x_move, y_move):
        self.x = x
        self.y = y
        
        self.x_move = x_move
        self.y_move = y_move
        
    def __eq__(self, other):
        if collision(self, other, 0):
            return True


class Snack:
    def __init__(self, x, y, color=(0, 255, 0)):
        self.x = x
        self.y = y
        self.color = color
        
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, SIDE, SIDE))
