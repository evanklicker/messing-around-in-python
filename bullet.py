import pygame
import math

GREY = (150, 150, 150)

class Bullet():
    def __init__(self, player, speed = 5):
        
        #These handle the basic attributes of each bullet
        self.direction = player.direction
        self.color = GREY
        self.speed = speed
        self.length = 6
        self.thickness = 3
        
        #These keep track of the bullet's position
        self.start_posx = player.posx
        self.start_posy = player.posy
        
        self.end_posx = self.start_posx
        self.end_posy = self.start_posy
        
        #This is to prevent the bullet from starting inside the player
        self.offset = player.radius
        
        #Each bullet has a frame counter separate from the main loop's
        #This is so they can expire and be created without having to rely on the main loop
        self.frame = 0
        self.frame_temp = 0
        
        #This is how many frames it takes for the bullets to "die"
        self.expiration_frame = 9
        
        #The bullets are create alive
        self.alive = True
        
    def draw(self, screen):
        
        #Easy enough
        pygame.draw.line(screen, self.color, [self.start_posx, self.start_posy], [self.end_posx, self.end_posy], self.thickness)
            
    def update(self, screen, player, frame):
        
        #Move the frame counter forward
        if self.frame_temp != frame:
            self.frame += 1
            self.frame_temp = frame
            
        #Reset the basic attributes, in case they were changed
        self.length = 5
        self.expiration_frame = 9
        
        #Change determinants based on direction
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
            
        #Since the hypotenuse of a triangle is longer than the other sides, we need to scale down the size to compensate
        #The bullet will travel faster, but should travel about the same distance in the given time.
        else:
            self.length = round(self.length / math.sqrt(2))
            self.expiration_frame = self.expiration_frame * 2 / 3
            
            #Once again, change determinants based on direction
            #I kept these checks in the else statement because:
                #1. It saves time if the player isn't going diagonally, and 
                #2. We only need to change the bullet length and expiration time if the bullet is going in one of these directions.
                
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
                
        #Calculate where to draw the bullet based on previous position, as well as the determinants, frame count, offset, and bullet length
        self.start_posx = self.start_posx + (x_determinant * (self.frame + self.offset))
        self.start_posy = self.start_posy + (y_determinant * (self.frame + self.offset))
        self.end_posx   = self.start_posx   + (x_determinant * (self.frame + self.offset + self.length))
        self.end_posy   = self.start_posy   + (y_determinant * (self.frame + self.offset + self.length))
        
        #If it's the bullet's time to die, it's the bullet's time to die
        if self.frame >= self.expiration_frame:
            self.alive = False
        return self.alive
            
