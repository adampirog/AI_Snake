import csv
import pygame 
import random
from datetime import datetime

from AI_sensors import get_equation, get_basic_vision, get_extended_vision, FAR
from classes import Snake, Snack, collision, WIDTH, HEIGHT

SCORE = 0

ENGINE = False

    
def spawn_snack():
    return (Snack(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)))


def draw_score(window, font):
    score_label = font.render("Score: " + str(SCORE), 1, (255, 255, 255))
    window.blit(score_label, (WIDTH - score_label.get_width() - 15, 10))


def save_score(filename):
    
    max_score = 0
    text = "HUMAN"
    if (ENGINE):
        text = "ENGINE"
        
    with open(filename, 'r') as file:
        reader = csv.reader(file, skipinitialspace=True)
        for row in reader:
            if(row[2] == text):
                scr = int(row[1][7:])
                if(scr > max_score):
                    max_score = scr

    if(SCORE > max_score):
        with open(filename, 'a') as file:
            file.write("\n" + datetime.now().strftime("%d-%m-%Y %H:%M:%S") + ", SCORE: " + str(SCORE))
            if(ENGINE):
                file.write(", ENGINE")
            else:
                file.write(", HUMAN")


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


def main():
    global SCORE
    
    run = True
    pygame.init()  
    pygame.font.init()
    
    snack = spawn_snack()
    player = Snake(WIDTH // 2, HEIGHT // 2, False)

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake")
    
    font = pygame.font.Font('freesansbold.ttf', 40)
    clock = pygame.time.Clock()
    
    while run:
        clock.tick(30)
        window.fill((0, 0, 0))
        draw_vision(window, player, snack)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_score('scoreboard.txt')
                run = False
                pygame.quit()
                quit()
                break
                
        # snack eating
        if(collision(player, snack, 15)):
            
            snack = spawn_snack()
            size = len(player.body)
            if(size == 1):
                SCORE += 1
            SCORE += (size - 1)
            
            player.add_cube()

        run = not player.move(window)
        snack.draw(window)
        draw_score(window, font)
        pygame.display.update()

    save_score('scoreboard.txt')
    draw_game_over(window, font)
    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
