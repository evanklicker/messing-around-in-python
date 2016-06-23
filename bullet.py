import pygame
import math

GREY = (150, 150, 150)

class Bullet():
    def __init__(self, player, speed = 5):
        
        self.direction = player.direction
        self.color = GREY
        self.speed = speed
        self.length = 6
        self.thickness = 3
        
        self.start_posx = player.posx
        self.start_posy = player.posy
        
        self.offset = player.radius
        
        self.end_posx = self.start_posx
        self.end_posy = self.start_posy
        
        self.frame = 0
        self.frame_temp = 0
        
        self.expiration_frame = 9
        
        self.alive = True
        
    def draw(self, screen):
        pygame.draw.line(screen, self.color, [self.start_posx, self.start_posy], [self.end_posx, self.end_posy], self.thickness)
            
    def update(self, screen, frame):
        if self.frame_temp != frame:
            self.frame += 1
            self.frame_temp = frame
        self.length = 5
        self.expiration_frame = 9
        if self.direction == "L":
            x_determinant = -1
            y_determinant = 0
        elif self.direction == "R":
            x_determinant = 1
            y_determinant = 0
        elif self.direction == "U":
            x_determinant = 0
            y_determinant = -1
        elif self.direction == "D":
            x_determinant = 0
            y_determinant = 1
        else:
            self.length = round(self.length / math.sqrt(2))
            self.expiration_frame = 6     
            if self.direction == "LU":
                x_determinant = -1
                y_determinant = -1
            elif self.direction == "RU":
                x_determinant = 1
                y_determinant = -1
            elif self.direction == "LD":
                x_determinant = -1
                y_determinant = 1
            elif self.direction == "RD":
                x_determinant = 1
                y_determinant = 1
        self.start_posx = self.start_posx + (x_determinant * (self.frame + self.offset))
        self.start_posy = self.start_posy + (y_determinant * (self.frame + self.offset))
        self.end_posx   = self.start_posx   + (x_determinant * (self.frame + self.offset + self.length))
        self.end_posy   = self.start_posy   + (y_determinant * (self.frame + self.offset + self.length))
        
        if self.frame >= self.expiration_frame:
            self.alive = False
        return self.alive
            
