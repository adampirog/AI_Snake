import pygame 
from classes import Snake, Snack, collision, WIDTH, HEIGHT
import random
from datetime import datetime

from AI_activation import get_basic_vision, get_extended_vision

SCORE = 0

ENGINE = False

    
def spawn_snack():
    return (Snack(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)))


def draw_score(window, font):
    score_label = font.render("Score: " + str(SCORE), 1, (255, 255, 255))
    window.blit(score_label, (WIDTH - score_label.get_width() - 15, 10))


def save_score(filename):
    if(SCORE > 0):
        with open(filename, 'a') as file:
            file.write("\n" + datetime.now().strftime("%d-%m-%Y %H:%M:%S") + ",   SCORE: " + str(SCORE))
            if(ENGINE):
                file.write(",    ENGINE")
            else:
                file.write(",    HUMAN")


def game_over(window, font):
     
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


def report(player, snack):
    result = get_basic_vision(player, snack)
    #print(result)
    
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
    player = Snake(WIDTH // 2, HEIGHT // 2)

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake")
    
    font = pygame.font.Font('freesansbold.ttf', 40)
    clock = pygame.time.Clock()
    
    while run:
        clock.tick(30)
        window.fill((0, 0, 0))
        report(player, snack)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_score('scoreboard')
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

    report(player, snack)
    #save_score('scoreboard')
    game_over(window, font)
    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
