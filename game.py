import pygame 
from classes import Snake


WIDTH = 600
HEIGHT = 600


def main():
    
    run = True
    pygame.init()  
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    player = Snake(WIDTH // 2, HEIGHT // 2)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Snake")

    while run:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        window.fill((0, 0, 0))
        player.move(window)
        pygame.display.update()

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
