import pygame
import math
import bullet as b
import sword as s
import inventory as i

GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
BROWN = (130,  94,  35)

class Player():
    def __init__(self, screen):
        
        #The player is, at this point, and circle.
        self.radius = 15
        self.move_speed = 3
        
        #Currently, this is the color of the edge of the circle. The inside is white.
        self.color = GREEN
        
        #So we can tell what direction the player is facing
        #This is the color used for the player's "eye"
        self.color2 = BLUE
        
        #Possible directions are Left (L), Right (R), Up (U), Down (D), Left-Up (LU), Left-Down (LD), Right-Up (RU), and Right-Down (RD)
        self.direction = "R"
        
        #Attributes for attacking
        self.attack_cooldown = 20 #frames
        self.cooldown_done = True
        self.attacking = False
        self.frame = 0
        self.frame_temp = 0
        
        #Attributes to keep track of player location
        self.posx = 100
        self.posy = 100
        self.changex = 0
        self.changey = 0
        
        #Let's get some items! We need an inventory first, though
        self.inventory = i.Inventory(screen)
        self.showing_inventory = False
        
        #A sword for our noble hero!
        self.inventory.get_item(s.Sword(self))
        self.equipped_main_hand = self.inventory.item_list[0]
        
        
        #A list for every bullet that exists
        self.bullet_list = [] 
            
        
        
    #Self explanatory
    def go_left(self):
        self.changex += -self.move_speed
        self.direction = "L"
        self.speed_check()
        
    def go_right(self):
        self.changex += self.move_speed
        self.direction = "R"
        self.speed_check()
            
    def go_up(self):
        self.changey += -self.move_speed
        self.direction = "U"
        self.speed_check()
                   
    def go_down(self):
        self.changey += self.move_speed
        self.direction = "D"
        self.speed_check
        
        
    #These functions basically just reverse the ones from above        
    def stop_left(self):
        self.changex += self.move_speed
        self.speed_check()
    
    def stop_right(self):
        self.changex += -self.move_speed
        self.speed_check()
        
    def stop_up(self):
        self.changey += self.move_speed
        self.speed_check()
        
    def stop_down(self):
        self.changey += -self.move_speed
        self.speed_check()
        
    def speed_check(self):
        if self.changex > 5:
            self.changex = 5
        elif self.changex < -5:
            self.changex = -5
        if self.changey > 5:
            self.changey = 5
        elif self.changey < -5:
            self.changey = -5
            
    def get_item(self, item):
        self.inventory.get_item(item)
        
    def update(self, screen, frame):
        
        """Code block for mainting on-screen position"""
        x_limit, y_limit = screen.get_size()
        newx = self.posx + self.changex
        newy = self.posy + self.changey
        
        #If our x value is within the bounds of the screen:
        if newx >= self.radius and newx < x_limit - self.radius + 1:
            self.posx = newx
            
        #If the x value isn't:
        elif newx < self.radius:
            self.posx = self.radius
        elif newx > x_limit - self.radius:
            self.posx = x_limit - self.radius
            
        #If our y value is within the bounds of the screen:
        if newy >= self.radius and newy  <= y_limit - self.radius:
            self.posy = newy
        
        #If the y value isn't:
        elif newy < self.radius - 1:
            self.posy = self.radius
        elif newy >= y_limit - self.radius + 2:
            self.posy = y_limit - self.radius
        
        """Code block for maintaining player direction"""  
          
        if self.changex < 0 and self.changey == 0:
            self.direction = "L"
        elif self.changex > 0 and self.changey == 0:
            self.direction = "R"
        elif self.changey < 0 and self.changex == 0:
            self.direction = "U"
        elif self.changey > 0 and self.changex == 0:
            self.direction = "D"
        elif self.changex < 0 and self.changey < 0:
            self.direction = "LU"
        elif self.changex < 0 and self.changey > 0:
            self.direction = "LD"
        elif self.changex > 0 and self.changey < 0:
            self.direction = "RU"
        elif self.changex > 0 and self.changey > 0:
            self.direction = "RD"
            
        #This code checks to see whether or not the player should be attacking
        if self.attacking:
            self.attack(screen, frame)
            
        #Checking to see if the bullets have expired. If not, update them!
        for bullet in self.bullet_list:
            if not bullet.update(screen, frame):
                self.bullet_list.remove(bullet)

        #Update every item's position
        for item in self.inventory.item_list:
            if item:
                item.update(screen, self, frame)
                #print("Item Updated!")
        
        #print("Inventory Updated!")

    def draw(self, screen, frame):
        
        #The variables are pretty self-explanatory. The 2 at the end should be replaced with self.border_width at some point
        pygame.draw.circle(screen, self.color, [self.posx, self.posy], self.radius, 2)
        
        #The following code draws the player's "eye" based on the direction the player is moving
        if self.direction == "L":
            pygame.draw.circle(screen, self.color2, [self.posx - (self.radius - 1) , self.posy], 1)
        if self.direction == "R":
            pygame.draw.circle(screen, self.color2, [self.posx + (self.radius - 1), self.posy], 1)
        if self.direction == "U":
            pygame.draw.circle(screen, self.color2, [self.posx, self.posy - (self.radius - 1)], 1)
        if self.direction == "D":
            pygame.draw.circle(screen, self.color2, [self.posx, self.posy + (self.radius - 1)], 1)
        if self.direction == "LU":
            pygame.draw.circle(screen, self.color2, [self.posx - round(self.radius / math.sqrt(2)), self.posy - round(self.radius / math.sqrt(2))], 1)
        if self.direction == "RU":
            pygame.draw.circle(screen, self.color2, [self.posx + round(self.radius / math.sqrt(2)), self.posy - round(self.radius / math.sqrt(2))], 1)
        if self.direction == "LD":
            pygame.draw.circle(screen, self.color2, [self.posx - round(self.radius / math.sqrt(2)), self.posy + round(self.radius / math.sqrt(2))], 1)
        if self.direction == "RD":
            pygame.draw.circle(screen, self.color2, [self.posx + round(self.radius / math.sqrt(2)), self.posy + round(self.radius / math.sqrt(2))], 1)
                      
        #Draw the bullets! All of 'em!           
        for bullet in self.bullet_list:
            bullet.draw(screen)
        
        if self.attacking:
            self.equipped_main_hand.attack_draw(screen)
        
        if self.showing_inventory:
            self.inventory.draw(screen)
            
    def attack(self, screen, frame):
        
        #There is still a bit of a glitch in this code. Every so often, a bullet doesn't fire when it should.
        #Probably something to do with the frame checking.
        
        #This code handles the player's frame separately from the game frames.
        if self.frame_temp != frame:
            self.frame += 1
            self.frame_temp = frame
            
        #If our attacking cooldown is done, then we can attack again!
        if self.cooldown_done:
            
            #If we wanted to shoot bullets, we'd do this code:
            
            print("Cooldown Done!")
            #bullet = b.Bullet(self)
            #self.cooldown_done = False
            #self.bullet_list.append(bullet)
            
            
            #Good thing we wanna swing a sword!
            self.equipped_main_hand.attacking = True
            self.cooldown_down = False
            
        #Resetting the cooldown based on the players frames.
        if self.frame == 19:
            self.cooldown_done = True
            self.frame = 0
            
