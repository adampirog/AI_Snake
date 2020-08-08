import pygame 
from classes import Snake, Snack, collision
import random

WIDTH = 600
HEIGHT = 600


def spawn_snack(snacks):
    snacks.append(Snack(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)))


def main():
    
    run = True
    pygame.init()  
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    player = Snake(WIDTH // 2, HEIGHT // 2)
    snacks = []
    spawn_snack(snacks)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Snake")

    while run:
        clock.tick(30)
        window.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        # snack eating
        for snack in list(snacks):
            snack.draw(window)
            if(collision(player, snack, 15)):
                snacks.remove(snack)
                player.add_cube()
                spawn_snack(snacks)
     
        player.move(window)
        pygame.display.update()

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
