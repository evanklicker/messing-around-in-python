import pygame
import math

BROWN = (130,  94,  35)
WHITE = (255, 255, 255)

class Sword(pygame.sprite.Sprite):
    def __init__(self, player):
        
        #This loads the image and converts it to a format pygame can work with easier
        self.image= pygame.image.load("./Items/woodensword_1.png").convert()
        #Image courtesy of opengameart.com
        #http://opengameart.org/content/swords-0
        
        #Note: this image naturally points toward the direction "Left-Up," 
        #This corresponds to an angle 135 degrees, or (3*pi)/4 radians, if you are so inclined
        #After the 180 degree rotation coming up, the image will be at an angle of -45 degrees, or -pi/4
        
        #A temp variable to store the individual transformations without too much loss of quality:
        self.rotated_image = pygame.transform.rotate(self.image, 180)
        
        self.image.set_colorkey(WHITE)
        
        #Since we're rotating from the corner, the image's x and y coordinate will need to be corrected
        #Rotate about the center of the player image
        self.x_offset = player.rect.x / 2
        self.y_offset = player.rect.y / 2
        
        self.rect = self.image.get_rect()
        
        #Each type is represented by a number
        #1 represents main hand
        #2 represents off hand
        #3 represents consumable
        #4 represents key item, or other
        self.item_type = 1
        
        #Base the initial positions on the player's positions
        self.hilt_posx = player.rect.x
        self.hilt_posy = player.rect.y
      
        self.direction = player.direction
        
        #Used to determine attack cooldown
        #Higher = faster
        #Similar to the dimensions, at some point, the "10" will be replaced with something like "sword_type.swing_speed"
        self.swing_speed = 10
        self.attacking = False
        
        #An independent frame counter, though we could probably use the player's frame counter, because there will only be one sword at a time
        self.frame = 0
        self.frame_temp = 0
        
        #Lastly, the number of frames it takes to swing the sword
        self.expiration_frame = round(200 / self.swing_speed)
        self.alive = True
        
    def draw(self, screen, pos):
        
        #This draw method is to be called by the inventory class, 
        #so as to remove the confusing between the player's attacking sword
        #And the inventory's static sword
        screen.blit(self.image, pos)
                    
    def attack_draw(self, screen, frame):
        
        #We always draw the rotated image, even if the sword isn't rotated. The update method should account for that.

        if self.attacking:
            screen.blit(self.rotated_image, [self.rect.x + self.x_offset, self.rect.y + self.y_offset])

    def update(self, screen, player, frame):
        """Change the sword's position and possilby direction based on the player's positioning, as well as the sword's own frame counter"""
        
        #We nab the info we need right away, and then have nothing to do with it after that
        #Also, we check to see if we even need to update the info. After all, if we can't see the sword, there's no need to update
        if self.attacking:
            
            #First, we want to make sure that the player and the sword are on the same page in terms of direction
            self.direction = player.direction
            
            #We also need to update the position such that it always follows the player
            self.rect.x = player.rect.x
            self.rect.y = player.rect.y
            
            self.x_offset = self.rect.width
            self.y_offset = self.rect.height
        
            #Then, we update our frame
                
            if self.frame_temp != frame:
                self.frame += 1
                self.frame_temp = frame
                        
            if self.frame >= self.expiration_frame:
                self.attacking = False
                self.frame = 0
              
            #We have to handle each direction separately
            #These angles represent the rotation that has to be done at the start of the animation
            #Every angle will end up being 90 degrees larger at the end of the animation
            #I also decided to keep all the angles between -180 and 180 degrees, 'cuz I can
            if    self.direction == "L":
                rotate_angle =  180 + (90 * self.frame / self.expiration_frame)
                self.x_offset = -self.rect.width
                self.y_offset = -self.rect.height / 4
            elif  self.direction == "R":
                rotate_angle =    0 + (90 * self.frame / self.expiration_frame)
                self.x_offset = 0
                self.y_offset = 0 #self.rect.height / 4
            elif  self.direction == "U":
                rotate_angle =   90 + (90 * self.frame / self.expiration_frame)
                self.x_offset = -self.rect.width / 2
                self.y_offset = -self.rect.height / 2
            elif  self.direction == "D":
                rotate_angle =  -90 + (90 * self.frame / self.expiration_frame)
                self.x_offset = -self.rect.width / 2
                self.y_offset = self.rect.height / 2
                
            rotate_angle += 180
                
            #We shouldn't need to reset the rotated image variable before this line is run
            self.rotated_image = pygame.transform.rotate(self.image, rotate_angle)
            
            #Finally, we check for expiration and reset our frame counter if we need to

