import pygame
import math
import copy
import time
import queue
import bullet as b
import sword as sw
import inventory as i
import shield as sh
import spritesheet as ss

GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
BROWN = (130,  94,  35)

class Player(pygame.sprite.Sprite):
    def __init__(self, screen, current_room):
        pygame.sprite.Sprite.__init__(self)
        
        #Possible directions are Left (L), Right (R), Up (U), Down (D), Left-Up (LU), Left-Down (LD), Right-Up (RU), and Right-Down (RD)
        #The diagonal directions will be leaving here shortly
        self.direction = "R"
        
        #Based on 
        self.draw_first = False
        
        #The higher, the slower, oddly enough
        #Should be called self.walking_slowness, haha
        self.walking_speed = 5
        
        #This will be false if the game is paused
        self.updating = False
        #Booleans for whether the player is moving Left, Right, Up, or Down
        self.moving = [False, False, False, False]
        
        #Player walking images
        self.walking_frames_u = []
        self.walking_frames_d = []
        self.walking_frames_l = []
        self.walking_frames_r = []
        
        #Which room are we in?
        self.room = current_room
        
        #Create our player image
        self.get_image()
        
        #Align the walking frames, and get our position
        self.image = self.walking_frames_r[0]
        self.rect = self.image.get_rect()
        
        #A queue to hold our movements
        self.movement_queue = []
        
        #Attributes for attacking
        self.attack_cooldown = 20 #frames
        self.cooldown_done = True
        self.attacking = False
        self.frame = 0
        self.frame_temp = 0
        self.walking_frame = 0
        
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
        self.direction = "L"
        self.room.entity_left(self)
        
    def go_right(self):
        self.direction = "R"
        self.room.entity_right(self)
        
    def go_up(self):
        self.direction = "U"
        self.room.entity_up(self)
        
    def go_down(self):
        self.direction = "D"
        self.room.entity_down(self)
            
    def get_room_pos(self):
        for column in range(self.room.tile_list.__len__()):
            for row in range(self.room.tile_list[column].__len__()):
                if self.room.tile_list[column][row].contained_entity == self:
                    return [column, row]
        return [0, 0] 
                
    def get_item(self, item):
        self.inventory.get_item(item)
        
    def change_room(self, room):
        self.room = room
        
    def collision_check(self):
        
        future_player = copy.copy(self)
        if self.direction == "L":
            future_player.rect.x -= self.rect.width
            if pygame.sprite.spritecollide(future_player, self.room.obstacle_list, False).__len__() > 0:
                return True
            else:
                return False
        
        elif self.direction == "R" :
            future_player.rect.x += self.rect.width
            if pygame.sprite.spritecollide(future_player, self.room.obstacle_list, False).__len__() > 0:
                return True
            else:
                return False
                
        elif self.direction == "U":
            future_player.rect.y -= self.rect.width
            if pygame.sprite.spritecollide(future_player, self.room.obstacle_list, False).__len__() > 0:
                return True
            else:
                return False                
        
        elif self.direction == "D":
            future_player.rect.y += self.rect.width
            if pygame.sprite.spritecollide(future_player, self.room.obstacle_list, False).__len__() > 0:
                return True
            else:
                return False    
    
    """To be added at some point            
    def movement_cooling_down(self, frame_left = 0):
        if frame_left > 0:
            return movement_cooling_down(frame_left - 1)
        return True
    """
    
    def update(self, screen, frame, current_room = None):
        
        #If we are supposed to be updating...
        if self.updating:
            
            if self.direction == "L":
                self.image_frames = self.walking_frames_l
            elif self.direction == "R":
                self.image_frames = self.walking_frames_r
            elif self.direction == "U":
                self.image_frames = self.walking_frames_u
            elif self.direction == "D":
                self.image_frames = self.walking_frames_d
                
            if frame == 0 or frame == 10:
                self.walking_frame += 1
                
            if self.walking_frame >= self.image_frames.__len__():
                self.walking_frame = 0
                
            self.image = self.image_frames[self.walking_frame]
                
            #Regardless of the image, we want it to be slightly smaller than the tile size, which happens to be 80x80 pixels
            self.image = pygame.transform.scale(self.image, [50, 70])
                
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
        
        #Lastly, make sure we align the player's room with the main class's room, if we need to
        if current_room:
            self.change_room(current_room)


    def draw(self, screen, x_offset = 0, y_offset = 0):
        
        #Draw the player if they are supposed to be drawn first
        if self.draw_first:
            screen.blit(self.image, [self.rect.x + x_offset, self.rect.y + y_offset])
           
        #Draw the bullets! All of 'em!           
        for bullet in self.bullet_list:
            bullet.draw(screen, x_offset, y_offset)
            
        if self.attacking and self.equipped_main_hand:
            self.equipped_main_hand.attack_draw(screen, x_offset, y_offset)
            
        #Or, draw the player if they aren't supposed to be drawn first    
        if not self.draw_first:
            screen.blit(self.image, [self.rect.x + x_offset, self.rect.y + y_offset])
            
        if self.showing_inventory:
            self.inventory.draw(screen)
            
        return True    
            
    def attack(self, screen, frame):
        
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
            #Something is wonky. This'll need to get fixed later
            if self.frame == 17:
                self.equipped_main_hand.attacking = False
                self.attacking = False
                self.cooldown_done = True
                self.frame = 0
            
    def get_image(self):
        #This loads and creates the walking frames to be used by the player
        
        sprite_sheet = ss.SpriteSheet("./player/mage_walking_sheet.png")
        #Spritesheet courtesy of Redshrike from opengameart.org
        #http://opengameart.org/content/four-characters-my-lpc-entries
        
        #I didn't like this frame, so I commented it out
        #image = sprite_sheet.get_image(16, 9, 32, 52)
        #self.walking_frames_u.append(image)
        
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

        image = sprite_sheet.get_image(17, 73, 30, 53)
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
        
        #Same thing as before- it looks dumb
        #image = sprite_sheet.get_image(16, 137, 32, 54)
        #self.walking_frames_d.append(image)
        
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
        
