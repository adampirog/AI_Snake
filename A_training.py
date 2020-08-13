import pygame 
from classes import Snake, Snack, collision, WIDTH, HEIGHT
import random
from datetime import datetime

import os
import neat
import joblib
from time import time
from AI_sensors import get_equation, get_basic_vision, get_extended_vision, FAR

SCORE = 0

ENGINE = False
START_TIME = 0
END_TIME = 300

GENERATION = 0

SPECIMEN = 0

    
def spawn_snack():
    return (Snack(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)))


def draw_score(window, font):
    score_label = font.render("Score: " + str(SCORE), 1, (255, 255, 255))
    window.blit(score_label, (WIDTH - score_label.get_width() - 15, 10))
   
 
def draw_progress(window, font, generation, specimen):
    score_label = font.render("Generation: " + str(generation) + " Specimen: " + str(specimen), 1, (255, 255, 255))
    window.blit(score_label, (3, 10))


def save_score(filename):
    if(SCORE > 0):
        with open(filename, 'a') as file:
            file.write("\n" + datetime.now().strftime("%d-%m-%Y %H:%M:%S") + ",   SCORE: " + str(SCORE))
            if(ENGINE):
                file.write(",    ENGINE")
            else:
                file.write(",    HUMAN")


def get_vis_color(vis_data, direction_index):
    GREEN = (0, 255, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    snack = vis_data[direction_index][1]
    tail = vis_data[direction_index][2]

    if tail == FAR and snack == FAR:
        return WHITE

    if tail == FAR:
        return GREEN

    if snack == FAR:
        return RED

    if snack < tail:
        return RED
    else:
        return RED


def draw_vision(window, player, snack):
    #directions2 = ['NE', 'SE', 'SW', 'NW']
    # NW,SW,SE,NE

    extended_data = get_extended_vision(player, snack)
    basic_data = get_basic_vision(player, snack)
    start_pos = (round(player.x), round(player.y))
    
    color = (255, 255, 255)

    #N
    color = get_vis_color(basic_data, 0)
    pygame.draw.line(window, color, start_pos, (round(player.x), 0), 2)
    #S
    color = get_vis_color(basic_data, 1)
    pygame.draw.line(window, color, start_pos, (round(player.x), 600), 2)

    #E
    color = get_vis_color(basic_data, 2)
    pygame.draw.line(window, color, start_pos, (600, round(player.y)), 2)
    #W
    color = get_vis_color(basic_data, 3)
    pygame.draw.line(window, color, start_pos, (0, round(player.y)), 2)

    eq = get_equation(player, "NE")
    end_x = 600
    end_y = round(eq[0] * end_x + eq[1])
    color = get_vis_color(extended_data, 0)
    pygame.draw.line(window, color, start_pos, (end_x, end_y), 1)

    eq = get_equation(player, "SE")
    end_x = 600
    end_y = round(eq[0] * end_x + eq[1])
    color = get_vis_color(extended_data, 1)
    pygame.draw.line(window, color, start_pos, (end_x, end_y), 1)

    eq = get_equation(player, "SW")
    end_x = -1
    end_y = round(eq[0] * end_x + eq[1])
    color = get_vis_color(extended_data, 2)
    pygame.draw.line(window, color, start_pos, (end_x, end_y), 1)

    eq = get_equation(player, "NW")
    end_x = -1
    end_y = round(eq[0] * end_x + eq[1])
    color = get_vis_color(extended_data, 3)
    pygame.draw.line(window, color, start_pos, (end_x, end_y), 1)


def draw_game_over(window, font):
     
    run = True
    
    while run:
        label = font.render("GAME OVER", 1, (255, 255, 255))
        window.blit(label, (round((WIDTH - label.get_width()) / 2), round((HEIGHT - label.get_height()) / 2)))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False


# testing function for the AI sensors
def report(player, snack):
    result = get_basic_vision(player, snack)
    #result = get_extended_vision(player, snack)
    print(result)
    
    for i in range(4):
        if(result[i][1] < 0):
            print("Bang: ", i)
            print(result)


def evaluate(genomes, config):
    global GENERATION, SPECIMEN
    
    pygame.init()  
    pygame.font.init()
    
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.Font('freesansbold.ttf', 30)
    font_small = pygame.font.Font('freesansbold.ttf', 15)
    pygame.display.set_caption("Snake")
    
    clock = pygame.time.Clock()
    
    GENERATION += 1
    SPECIMEN = 0
    
    for _, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = 0
        
        is_alive = True
        SPECIMEN += 1
        
        snack = spawn_snack()
        player = Snake(WIDTH // 2, HEIGHT // 2, True)
        framerate = 200
        
        while(is_alive):
            clock.tick(framerate)
            window.fill((0, 0, 0))
            #draw_vision(window, player, snack)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    break
            
            # fitness per frame
            genome.fitness += (1 / (framerate * 1))
                                
            # snack eating
            if(collision(player, snack, 15)):
                snack = spawn_snack()
                size = len(player.body)
                if(size == 1):
                    genome.fitness += 1
                genome.fitness += (size - 1)
                
                player.add_cube()

            #moving the snake
            vision_sensors = get_basic_vision(player, snack) + get_extended_vision(player, snack)
            #print(vision_sensors[0])
            
            input_list = []
            for x in range(8):
                for y in range(3):
                    input_list.append(vision_sensors[x][y])
            
            output = net.activate(input_list)
            index = output.index(max(output))
            #print(output)
            
            if index == 0: 
                player.up()
            elif index == 1: 
                player.down()
            if index == 2: 
                player.right()
            if index == 3: 
                player.left()
                
            is_alive = not player.update_position(window)
                
            snack.draw(window)
            draw_score(window, font)
            draw_progress(window, font_small, GENERATION, SPECIMEN)
            pygame.display.update()


def run(config_file):
    global START_TIME
    
    START_TIME = time()
    
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(evaluate, 50)
    
    joblib.dump(winner, "Specimen001")
    print('\nBest genome:\n{!s}'.format(winner))
    print("Training time:", time() - START_TIME)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config")
    run(config_path)
    