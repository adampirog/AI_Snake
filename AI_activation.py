from classes import SIDE, HEIGHT, WIDTH
from classes import Snack
import numpy as np
from time import time

TOLLERANCE = 15
FAR = 1000


def timer(func):
    def wrapper(*args, **kwargs):
        before = time()
        result = func(*args, **kwargs)
        after = time()
        print("Elapsed: ", after - before)
        return result
    return wrapper


def get_equation(obj, direction):

    A = None
    B = None
    
    if(direction == 'W' or direction == 'E'):
        return np.array([0, obj.y])
        
    elif(direction == 'N' or direction == 'S'):
        return np.array([obj.x, 0])
    
    elif(direction == 'NE' or direction == 'SW'):
        A = np.array([[obj.x, 1], [obj.x + 1, 1]])
        B = np.array([obj.y, obj.y + 1])
    
    elif(direction == 'SE' or direction == 'NW'):
        A = np.array([[obj.x, 1], [obj.x - 1, 1]])
        B = np.array([obj.y, obj.y + 1])
        
    return np.round(np.linalg.solve(A, B))


def distance_from_line(obj, eq):
    if(eq[0] == 0):
        return abs(eq[1] - obj.y)
    elif(eq[1] == 0):
        return abs(eq[0] - obj.x)
    return round(abs((eq[0] * obj.x) + eq[1] - obj.y) / np.sqrt(np.square(eq[0]) + 1))


def distance_from_object(cube1, cube2):
    en = np.array([cube1.x, cube1.y])
    ms = np.array([cube2.x, cube2.y])

    return np.linalg.norm(en - ms)

  
# static vectors. up, down, right, letf ;  0 - wall, 1 - snack, 2 -player
def get_basic_vision(player, snack):
    up = []
    
    # wall
    up.append(player.y)
    
    #snack
    if((abs(player.x - snack.x) <= TOLLERANCE) and (snack.y < player.y)):
        up.append(abs(player.y - snack.y) - SIDE)
    else:
        up.append(FAR)
        
    #body
    for i, cube in enumerate(player.body):
        if(i > 1):
            if((abs(player.x - cube.x) <= TOLLERANCE) and (cube.y < player.y)):
                up.append(abs(player.y - cube.y) - SIDE)
                break
    if (len(up) == 2):
        up.append(FAR)
      
    # down section    
    down = []
    
    # wall
    down.append(HEIGHT - player.y - SIDE)
    
    #snack
    if((abs(player.x - snack.x) <= TOLLERANCE) and (snack.y > player.y)):
        down.append(abs(player.y - snack.y) - SIDE)
    else:
        down.append(FAR)
        
    #body
    for i, cube in enumerate(player.body):
        if(i > 1):
            if((abs(player.x - cube.x) <= TOLLERANCE) and (cube.y > player.y)):
                down.append(abs(player.y - cube.y) - SIDE)
                break
    if (len(down) == 2):
        down.append(FAR)
        
    # left section    
    left = []
    
    left.append(player.x)
    
    #snack
    if((abs(player.y - snack.y) <= TOLLERANCE) and (snack.x < player.x)):
        left.append(abs(player.x - snack.x) - SIDE)
    else:
        left.append(FAR)
        
    #body
    for i, cube in enumerate(player.body):
        if(i > 1):
            if((abs(player.y - cube.y) <= TOLLERANCE) and (cube.x < player.x)):
                left.append(abs(player.x - cube.x) - SIDE)
                break
    if (len(left) == 2):
        left.append(FAR)
        
    # right section    
    right = []
    
    right.append(WIDTH - player.x - SIDE)
    
    #snack
    if((abs(player.y - snack.y) <= TOLLERANCE) and (snack.x > player.x)):
        right.append(abs(player.x - snack.x) - SIDE)
    else:
        right.append(FAR)
        
    #body
    for i, cube in enumerate(player.body):
        if(i > 1):
            if((abs(player.y - cube.y) <= TOLLERANCE) and (cube.x > player.x)):
                right.append(abs(player.x - cube.x) - SIDE)
                break
    if (len(right) == 2):
        right.append(FAR)
        
    return [up, down, right, left]

 
# basic vectors rotated 45deg right
def get_extended_vision(player, snack):
    eq1 = get_equation(player, "NE")
    eq2 = get_equation(player, "SE")
    
    right_up = []
    eq = eq1
    corner = Snack(600, 0)
    
    # wall
    right_up.append(distance_from_object(player, corner) - SIDE)
    
    #snack
    if((distance_from_line(player, eq) <= TOLLERANCE) and (snack.y < player.y)):
        right_up.append(distance_from_object(player, snack) - SIDE)
    else:
        right_up.append(FAR)
        
    #body
    for i, cube in enumerate(player.body):
        if(i > 1):
            if((distance_from_line(cube, eq) <= TOLLERANCE) and (cube.y < player.y)):
                right_up.append(distance_from_object(player, cube) - SIDE)
                break
    if (len(right_up) == 2):
        right_up.append(FAR)
      
    # down section    
    right_down = []
    eq = eq2
    corner = Snack(600, 600)
    
    # wall
    right_down.append(distance_from_object(player, corner) - SIDE)
    
    #snack
    if((distance_from_line(player, eq) <= TOLLERANCE) and (snack.y > player.y)):
        right_down.append(distance_from_object(player, snack) - SIDE)
    else:
        right_down.append(FAR)
        
    #body
    for i, cube in enumerate(player.body):
        if(i > 1):
            if((distance_from_line(player, eq) <= TOLLERANCE) and (cube.y > player.y)):
                right_down.append(distance_from_object(player, cube) - SIDE)
                break
    if (len(right_down) == 2):
        right_down.append(FAR)
        
    # left section    
    left_down = []
    eq = eq1
    corner = Snack(0, 600)
    
    # wall
    left_down.append(distance_from_object(player, corner) - SIDE)
    
    #snack
    if((distance_from_line(player, eq) <= TOLLERANCE) and (snack.y > player.y)):
        left_down.append(distance_from_object(player, snack) - SIDE)
    else:
        left_down.append(FAR)
        
    #body
    for i, cube in enumerate(player.body):
        if(i > 1):
            if((distance_from_line(cube, eq) <= TOLLERANCE) and (cube.y > player.y)):
                left_down.append(distance_from_object(player, cube) - SIDE)
                break
    if (len(left_down) == 2):
        left_down.append(FAR)
        
    # left section    
    left_up = []
    eq = eq2
    corner = Snack(0, 0)
    
    # wall
    left_up.append(distance_from_object(player, corner) - SIDE)
    
    #snack
    if((distance_from_line(player, eq) <= TOLLERANCE) and (snack.y < player.y)):
        left_up.append(distance_from_object(player, snack) - SIDE)
    else:
        left_up.append(FAR)
        
    #body
    for i, cube in enumerate(player.body):
        if(i > 1):
            if((distance_from_line(cube, eq) <= TOLLERANCE) and (cube.y < player.y)):
                left_up.append(distance_from_object(player, cube) - SIDE)
                break
    if (len(left_up) == 2):
        left_up.append(FAR)
        
    return [right_up, right_down, left_down, left_up]


def main():
    obj = Snack(456, 222)
    obj2 = Snack(33, 123)
        
    print(distance_from_object(obj, obj2))


if __name__ == "__main__":
    main()
