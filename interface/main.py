import pygame, sys
import serial
from settings import *
from sonar import Sonar
from utilities import get_pos_from_distance
from debug import debug

def parse_data(data):
    out = []
    decoded_data = data.split(",")
    for value in decoded_data:
        if value:
            out.append(int(value))
    return out

if __name__ == "__main__":

    arduino = serial.Serial("COM3", 9600, timeout=.1)

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None,30)
    running = True

    center = (SCREEN_WIDTH/2, SCREEN_HEIGHT)
    radius = 600
    sonar_screen = Sonar(center, radius, "#07cf00", view_angle=1)

    distance = 0
    angle = 0

    while running:
        data = parse_data(arduino.readline().decode("utf-8"))
        if data:
            distance, angle = data

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

        y_pos = 0
        if distance <= 40:
            y_pos = get_pos_from_distance(distance, 40, center, radius)
            sonar_screen.add_detection_line(y_pos, angle)

        sonar_screen.update_scanline(angle)

        debug("Angle: " + str(round(angle, 1)))
        debug("Distance: " + str(distance), 50)
        # debug(str(pygame.mouse.get_pos()), 100)

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(FPS)  # limits FPS to 60

    arduino.close()
    pygame.quit()
    sys.exit()