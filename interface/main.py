import pygame, sys
import math
from settings import *
from sonar import Sonar
from debug import debug

if __name__ == "__main__":
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None,30)
    running = True

    center = (SCREEN_WIDTH/2, SCREEN_HEIGHT)

    sonar_screen = Sonar(center, 600, "#07cf00", view_angle=1)

    angle = 0
    direction = 1

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                sonar_screen.add_detection_line(pygame.mouse.get_pos()[1], angle)
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("#000000")

        # RENDER YOUR GAME HERE

        sonar_screen.draw()

        sonar_screen.update_scanline(angle)

        debug("Angle: " + str(round(angle, 1)))
        angle += 0.4 * direction
        if angle >= 180 or angle <= 0:
            direction *= -1

        # debug(pygame.mouse.get_pos(), 50)

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(FPS)  # limits FPS to 60

    pygame.quit()
    sys.exit()