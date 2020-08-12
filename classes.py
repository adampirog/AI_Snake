import pygame
import numpy as np
from time import time


WIDTH = 600
HEIGHT = 600

SIDE = 15

VEL = 4


def collision(cube1, cube2, tollerance=0):

    en = np.array([cube1.x, cube1.y])
    ms = np.array([cube2.x, cube2.y])

    dist = np.linalg.norm(en - ms)

    if(dist <= tollerance):
        return True
    return False


# class to set a minimum time interval between function calls
class Lock:
    def __init__(self, time_interval):
        self.time_interval = time_interval
        self.start_time = 0
        
    def lock(self):
        self.start_time = time()
        
    def isLocked(self):
        if((time() - self.start_time) >= self.time_interval):
            return False
        else:
            return True


# decorator to make a function secure with a Lock class
def secure_function(lock):
    def decorator(function):
        def wrapper(*args, **kwargs):
            result = None
            if(not lock.isLocked()):
                result = function(*args, **kwargs)
                lock.lock()
            return result
        return wrapper
    return decorator


# global key lock
GKL = Lock(0.12)


class Cube:
    
    def __init__(self, x, y, x_move, y_move, color=(255, 0, 0)):
        self.x = x
        self.y = y
        self.color = color

        self.x_move = x_move
        self.y_move = y_move
           
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, SIDE, SIDE)) 
        
    def draw_head(self, window):
        eye_color = (0, 0, 255)
        pygame.draw.rect(window, self.color, (self.x, self.y, SIDE, SIDE)) 
        
        pygame.draw.circle(window, eye_color, ((self.x + SIDE // 2) - 3, (self.y + SIDE // 2) - 2), 2, 0)
        pygame.draw.circle(window, eye_color, ((self.x + SIDE // 2) + 3, (self.y + SIDE // 2) - 2), 2, 0)
        
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
    
    def __init__(self, x, y, setup=False):
        self.x = x
        self.y = y
        
        self.x_move = 0
        self.y_move = 0
        
        self.body = [Cube(x, y, 0, 0)]
        self.turns = []
        
        if(setup):

            self.up()
  
    def move(self, window):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_h]:
            self.left()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d] or keys[pygame.K_l]:
            self.right()
            
        if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_k]:
            self.up()
            
        if keys[pygame.K_DOWN] or keys[pygame.K_s] or keys[pygame.K_j]:
            self.down()
            
        if keys[pygame.K_p]:
            self.stop(window)
            
        if keys[pygame.K_o]:
            self.go(window)

        return self.update_position(window)
             
    @secure_function(GKL)
    def right(self):
        if(self.x_move != 0 and self.y_move == 0):
            return
        self.x_move = VEL
        self.y_move = 0
        self.turns.append(Turn(self.x, self.y, self.x_move, self.y_move))
        
    @secure_function(GKL)
    def left(self):
        if(self.x_move != 0 and self.y_move == 0):
            return
        self.x_move = -VEL
        self.y_move = 0
        self.turns.append(Turn(self.x, self.y, self.x_move, self.y_move))
       
    @secure_function(GKL)    
    def up(self):
        if(self.x_move == 0 and self.y_move != 0):
            return
        self.x_move = 0
        self.y_move = -VEL
        self.turns.append(Turn(self.x, self.y, self.x_move, self.y_move))
    
    @secure_function(GKL)
    def down(self):
        if(self.x_move == 0 and self.y_move != 0):
            return
        self.x_move = 0
        self.y_move = VEL
        self.turns.append(Turn(self.x, self.y, self.x_move, self.y_move))
    
    def update_position(self, window):
        
        self.x += self.x_move
        self.y += self.y_move
        
        for i, cube in enumerate(self.body):
            cube.update_position()
            if(i == 0):
                cube.draw_head(window)
            else:
                cube.draw(window)
            
            if(collision(self, cube, 16) and i != 0 and i != 1):
                return True

            for turn in list(self.turns):
                if collision(turn, cube):
                    cube.move(turn.x_move, turn.y_move)
                    if(i == len(self.body) - 1):
                        self.turns.remove(turn)

        if(self.x < 0):
            #self.x = WIDTH
            return True
        elif(self.x >= WIDTH - SIDE):
            #self.x = 0
            return True

        if(self.y < 0):
            #self.y = HEIGHT
            return True
        elif(self.y >= HEIGHT - SIDE):
            #self.y = 0
            return True

        return False
    
    def stop(self, window):
        self.x_move = 0
        self.y_move = 0
        
        self.update_position(window)
        
        for item in self.body:
            item.x_move = 0
            item.y_move = 0
            
    def go(self, window):
        self.x_move = 0
        self.y_move = -VEL
        
        self.update_position(window)
        
        for item in self.body:
            item.x_move = 0
            item.y_move = -VEL

    def add_cube(self):
        
        tail = self.body[-1]
        
        if(tail.x_move == 0):
            if(tail.y_move > 0):
                self.body.append(Cube(tail.x, (tail.y) - SIDE - 1, tail.x_move, tail.y_move))     
            else:
                self.body.append(Cube(tail.x, (tail.y) + SIDE + 1, tail.x_move, tail.y_move))  

        elif(tail.y_move == 0):
            if(tail.x_move > 0):
                self.body.append(Cube((tail.x) - SIDE - 1, tail.y, tail.x_move, tail.y_move))
            else:
                self.body.append(Cube((tail.x) + SIDE + 1, tail.y, tail.x_move, tail.y_move))
                

class Turn:
    def __init__(self, x, y, x_move, y_move):
        self.x = x
        self.y = y
        
        self.x_move = x_move
        self.y_move = y_move


class Snack:
    def __init__(self, x, y, color=(0, 255, 0)):
        self.x = x
        self.y = y
        self.color = color
        
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, SIDE, SIDE))
