import pygame
from utilities import get_pos_from_angle
from math import radians

pygame.init()
font = pygame.font.Font(None,30)

class Sonar():
    def __init__(self, center, radius, color, view_angle = 4, start_angle = 0):
        self.center = center
        self.radius = radius
        self.color = color

        self.scan_view_angle = view_angle
        self.scan_angle = start_angle

        self.detection_lines = []

        self.display_surface = pygame.display.get_surface()

    def draw_circles(self):
        i = 0.2
        while True:
            r = self.radius * i
            pygame.draw.circle(self.display_surface, self.color, self.center, r, width=2)
            i += 0.2
            if i > 1.0:
                break

    def draw_labels(self):
        for degree in range(0, 181, 15):
            x, y = get_pos_from_angle(self.center, degree, self.radius + 20)
            pygame.draw.line(self.display_surface, self.color, self.center, (x, y))
            self.draw_label_text(degree, (x, y))

    def draw_label_text(self, degree, pos):
        x, y = pos
        debug_surf = font.render(str(degree) + "°",True, self.color)
        debug_rect = debug_surf.get_rect(midbottom = (x,y))
        self.display_surface.blit(debug_surf,debug_rect)

    def draw_scanline(self):
        rect = pygame.Rect(self.center, (0, 0)).inflate(((self.radius*2) - 5, (self.radius*2) - 4))
        surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.arc(surf, (204, 6, 23, 100), surf.get_rect(), radians(self.scan_angle - (self.scan_view_angle/2)), radians(self.scan_angle + (self.scan_view_angle/2)), self.radius - 10)
        self.display_surface.blit(surf, rect)

    def update_scanline(self, degree):
        self.scan_angle = degree

    def add_detection_line(self, pos, angle):
        dl = DetectionLine(pos, angle, self.center, self.radius, (255, 0, 0, 255))
        self.detection_lines.append(dl)

    def draw_detection_lines(self):
        for idx, line in enumerate(self.detection_lines):
            if line.alpha <= 0:
                self.detection_lines.pop(idx)
                continue
            line.draw()
            line.update()

    def draw(self):
        self.draw_circles()
        self.draw_labels()
        self.draw_detection_lines()
        self.draw_scanline()

class DetectionLine():
    def __init__(self, distance, angle, circle_center, circle_radius, color):
        self.distance = distance
        self.angle = angle
        self.center = circle_center
        self.radius = circle_radius
        self.color = color
        self.alpha = 255

        self.pos1 = get_pos_from_angle(self.center, self.angle, self.center[1] - self.distance)
        self.pos2 = get_pos_from_angle(self.center, self.angle, self.radius)

        z = tuple(zip(self.pos1, self.pos2))
        min_x, max_x = sorted(z[0])
        min_y, max_y = sorted(z[1])

        if max_x - min_x < 1:
            max_x += 2
            min_x -= 2
        elif max_y - min_y < 1:
            max_y += 2
            min_y -= 2

        self.rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
        self.surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)

        self.display_surface = pygame.display.get_surface()

    def update(self):
        self.alpha -= 2

    def draw(self):

        # radius should be distance of mouse click from center
        #pygame.draw.rect(self.surface, "#0000ff", self.surface.get_rect())
        if self.angle < 90:
            pygame.draw.line(self.surface, (255, 0, 0, self.alpha), self.surface.get_rect().topright, self.surface.get_rect().bottomleft, 3)
        elif self.angle > 90:
            pygame.draw.line(self.surface, (255, 0, 0, self.alpha), self.surface.get_rect().topleft, self.surface.get_rect().bottomright, 3)
        else:
            pygame.draw.line(self.surface, (255, 0, 0, self.alpha), self.surface.get_rect().midtop, self.surface.get_rect().midbottom, 3)
        self.display_surface.blit(self.surface, self.rect)
