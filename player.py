import pygame
import math
import bullet as b
import sword as sw
import inventory as i
import shield as sh
import spritesheet as ss

GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
BROWN = (130,  94,  35)

class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        
        #Possible directions are Left (L), Right (R), Up (U), Down (D), Left-Up (LU), Left-Down (LD), Right-Up (RU), and Right-Down (RD)
        #The diagonal directions will be leaving here shortly
        self.direction = "R"
        
        #How fast the player moves
        self.move_speed = 3
        
        #Player walking images
        self.walking_frames_u = []
        self.walking_frames_d = []
        self.walking_frames_l = []
        self.walking_frames_r = []
        
        #Player images
        sprite_sheet = ss.SpriteSheet("./player/mage_walking_sheet.png")
        #Spritesheet courtesy of Redshrike from opengameart.org
        #http://opengameart.org/content/four-characters-my-lpc-entries
        image = sprite_sheet.get_image(16, 9, 32, 52)
        self.walking_frames_u.append(image)
        image = sprite_sheet.get_image(80, 9, 32, 52)
        self.walking_frames_u.append(image)
        image = sprite_sheet.get_image(144, 9, 33, 53)
        self.walking_frames_u.append(image)
        image = sprite_sheet.get_image(208, 10, 31, 53)
        self.walking_frames_u.append(image)
        image = sprite_sheet.get_image(272, 9, 32, 54)
        self.walking_frames_u.append(image)
        image = sprite_sheet.get_image(336, 9, 32, 52)
        self.walking_frames_u.append(image)
        image = sprite_sheet.get_image(400, 9, 32, 53)
        self.walking_frames_u.append(image)
        image = sprite_sheet.get_image(465, 10, 31, 53)
        self.walking_frames_u.append(image)
        image = sprite_sheet.get_image(528, 9, 32, 54)
        self.walking_frames_u.append(image)

        image = sprite_sheet.get_image(17, 72, 30, 53)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(81, 74, 30, 52)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(145, 73, 30, 52)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(209, 73, 30, 53)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(273, 73, 30, 53)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(337, 74, 31, 52)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(401, 73, 30, 53)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(465, 73, 30, 53)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(529, 73, 30, 53)
        self.walking_frames_l.append(image)
        
        image = sprite_sheet.get_image(16, 137, 32, 54)
        self.walking_frames_d.append(image)
        image = sprite_sheet.get_image(80, 137, 32, 54)
        self.walking_frames_d.append(image)
        image = sprite_sheet.get_image(145, 137, 32, 55)
        self.walking_frames_d.append(image)
        image = sprite_sheet.get_image(209, 138, 31, 54)
        self.walking_frames_d.append(image)
        image = sprite_sheet.get_image(272, 137, 33, 55)
        self.walking_frames_d.append(image)
        image = sprite_sheet.get_image(336, 137, 32, 53)
        self.walking_frames_d.append(image)
        image = sprite_sheet.get_image(400, 137, 33, 53)
        self.walking_frames_d.append(image)
        image = sprite_sheet.get_image(464, 138, 32, 54)
        self.walking_frames_d.append(image)
        image = sprite_sheet.get_image(528, 137, 32, 54)
        self.walking_frames_d.append(image)      

        image = sprite_sheet.get_image(17, 201, 30, 53)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(81, 202, 30, 52)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(145, 201, 30, 52)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(209, 201, 30, 53)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(273, 201, 30, 53)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(336, 202, 31, 52)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(401, 201, 30, 53)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(465, 201, 30, 53)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(529, 201, 30, 53)
        self.walking_frames_r.append(image)
        
        self.image = self.walking_frames_r[0]
        self.rect = self.image.get_rect()
        
        #Attributes for attacking
        self.attack_cooldown = 20 #frames
        self.cooldown_done = True
        self.attacking = False
        self.frame = 0
        self.frame_temp = 0
        
        #Attributes to keep track of player location
        self.changex = 0
        self.changey = 0
        
        #Let's get some items! We need an inventory first, though
        self.inventory = i.Inventory(screen)
        self.showing_inventory = False
        
        #A sword for our noble hero!
        #And a shield!
        self.get_item(sw.Sword(self))
        self.get_item(sh.Shield(self))
        self.equipped_main_hand = self.inventory.slot_list[8]
        self.equipped_off_hand  = self.inventory.slot_list[9]
        
        #A list for every bullet that exists
        self.bullet_list = [] 
            
    #Self explanatory
    def go_left(self):
        self.changex += -self.move_speed
        self.speed_check()
        
    def go_right(self):
        self.changex += self.move_speed
        self.speed_check()
            
    def go_up(self):
        self.changey += -self.move_speed
        self.speed_check()
                   
    def go_down(self):
        self.changey += self.move_speed
        self.speed_check
        
        
    #These functions basically just reverse the ones from above        
    def stop_left(self):
        if self.changex != 0:
            self.changex += self.move_speed
        self.speed_check()
    
    def stop_right(self):
        if self.changex != 0:
            self.changex += -self.move_speed
        self.speed_check()
        
    def stop_up(self):
        if self.changey != 0:
            self.changey += self.move_speed
        self.speed_check()
        
    def stop_down(self):
        if self.changey != 0:
            self.changey += -self.move_speed
        self.speed_check()
        
    def stop(self):
        #This stops all movement, period
        self.changex = 0
        self.changey = 0
        self.attacking = False
        
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
        newx = self.rect.x + self.changex
        newy = self.rect.y + self.changey
        
        #If our x value is within the bounds of the screen:
        if newx >= 0 and newx < x_limit - self.rect.width:
            self.rect.x = newx
            
        #If the x value isn't:

        elif newx < 0:
            self.rect.x = 0
        elif newx > x_limit - self.rect.width:
            self.rect.x = x_limit - self.rect.width
            
        #If our y value is within the bounds of the screen:
        if newy >= 0 and newy  <= y_limit - self.rect.height:
            self.rect.y = newy
        
        #If the y value isn't:
        elif newy < 0:
            self.rect.y = 0.
        elif newy >= y_limit - self.rect.height:
            self.rect.y = y_limit - self.rect.height
        
        """Code block for maintaining player direction"""  
          
        if self.changex < 0 and self.changey == 0:
            self.direction = "L"
        elif self.changex > 0 and self.changey == 0:
            self.direction = "R"
        elif self.changey < 0 and self.changex == 0:
            self.direction = "U"
        elif self.changey > 0 and self.changex == 0:
            self.direction = "D"

            
        """Code block for maintaining walking frames"""    

        if self.direction == "U":
            walking_frame = (self.rect.y // 30) % len(self.walking_frames_u)
            self.image = self.walking_frames_u[walking_frame]
        elif self.direction == "D":
            walking_frame = (self.rect.y // 30) % len(self.walking_frames_d)
            self.image = self.walking_frames_d[walking_frame]
        elif self.direction == "R":
            walking_frame = (self.rect.x // 30) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[walking_frame]
        elif self.direction == "L":
            walking_frame = (self.rect.x // 30) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[walking_frame]
            
        #This code checks to see whether or not the player should be attacking
        if self.attacking and self.equipped_main_hand:
            self.attack(screen, frame)
            
        #Checking to see if the bullets have expired. If not, update them!
        for bullet in self.bullet_list:
            if not bullet.update(screen, frame):
                self.bullet_list.remove(bullet)

        #Update every item's position
        for item in self.inventory.item_list:
            if item:
                item.update(screen, self, frame)
        
        self.equipped_main_hand = self.inventory.slot_list[8].contained_item
        self.equipped_off_hand  = self.inventory.slot_list[9].contained_item

    def draw(self, screen, frame):
        
        #The variables are pretty self-explanatory. The 2 at the end should be replaced with self.border_width at some point
        screen.blit(self.image, [self.rect.x, self.rect.y])
           
        #Draw the bullets! All of 'em!           
        for bullet in self.bullet_list:
            bullet.draw(screen)
        
        if self.attacking and self.equipped_main_hand:
            self.equipped_main_hand.attack_draw(screen, frame)
        
        if self.showing_inventory:
            self.inventory.draw(screen)
            
    def attack(self, screen, frame):
        
        #There is still a bit of a glitch in this code. Every so often, an animation gets skipped.
        #Probably something to do with the frame checking.
        
        if self.equipped_main_hand:
        
            #This code handles the player's frame separately from the game frames.
            if self.frame_temp != frame:
                self.frame += 1
                self.frame_temp = frame
            
            #If our attacking cooldown is done, then we can attack again!
            if self.cooldown_done:
            
                #If we wanted to shoot bullets, we'd do this code:
            
                #bullet = b.Bullet(self)
                #self.cooldown_done = False
                #self.bullet_list.append(bullet)
            
            
                #Good thing we wanna swing a sword!
                self.equipped_main_hand.attacking = True
                self.cooldown_down = False
            
            #Resetting the cooldown based on the players frames.
            if self.frame == 19:
                self.equipped_main_hand.attacking = False
                print(self.equipped_main_hand.attacking)
                self.cooldown_done = True
                self.frame = 0
            
