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
    def __init__(self, screen, current_room):
        pygame.sprite.Sprite.__init__(self)
        
        #Possible directions are Left (L), Right (R), Up (U), Down (D), Left-Up (LU), Left-Down (LD), Right-Up (RU), and Right-Down (RD)
        #The diagonal directions will be leaving here shortly
        self.direction = "R"
        
        #Based on 
        self.draw_first = False
        
        #How fast the player moves
        self.move_speed = 3
        #The higher, the slower, oddly enough
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
        
        #
        self.image = self.walking_frames_r[0]
        self.rect = self.image.get_rect()
        
        #Just so we don't run into anything weird, let's start a bit off the origin
        self.rect.x = 100
        self.rect.y = 100
        
        
        #Attributes for attacking
        self.attack_cooldown = 20 #frames
        self.cooldown_done = True
        self.attacking = False
        self.frame = 0
        self.frame_temp = 0
        
        #Attributes to keep track of player location
        self.change_x = 0
        self.change_y = 0
        
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
        self.change_x += -self.move_speed
        self.speed_check()
        self.direction = "L"
         
    def go_right(self):
        self.change_x += self.move_speed
        self.speed_check()
        self.direction = "R"
            
    def go_up(self):
        self.change_y += -self.move_speed
        self.speed_check()
        self.direction = "U"
         
    def go_down(self):
        self.change_y += self.move_speed
        self.speed_check()
        self.direction = "D"
          
    #These functions basically just reverse the ones from above        
    def stop_left(self):
        if self.change_x != 0:
            self.change_x += self.move_speed
        self.speed_check()
    
    def stop_right(self):
        if self.change_x != 0:
            self.change_x += -self.move_speed
        self.speed_check()
        
    def stop_up(self):
        if self.change_y != 0:
            self.change_y += self.move_speed
        self.speed_check()
        
    def stop_down(self):
        if self.change_y != 0:
            self.change_y += -self.move_speed
        self.speed_check()
        
    def stop(self):
        #This stops all movement, period
        self.change_x = 0
        self.change_y = 0
        self.attacking = False
        
    def speed_check(self):
        if self.change_x > self.move_speed:
            self.change_x = self.move_speed
        elif self.change_x < -self.move_speed:
            self.change_x = -self.move_speed
        if self.change_y >= self.move_speed:
            self.change_y = self.move_speed
        elif self.change_y < -self.move_speed:
            self.change_y = -self.move_speed
            
    def get_item(self, item):
        self.inventory.get_item(item)
        
    def change_room(self, room):
        self.room = room
        
        
    def update(self, screen, frame, current_room = None):
        
        #If we are supposed to be updating...
        if self.updating:
            
            if self.moving[0]:
                self.go_left()
            else:
                self.stop_left()
            if self.moving[1]:
                self.go_right()
            else:
                self.stop_right()
            if self.moving[2]:
                self.go_up()
            else:
                self.stop_up()
            if self.moving[3]:
                self.go_down()
            else:
                self.stop_down()
                
            """Code block for mainting on-screen position"""
            x_limit, y_limit = screen.get_size()
            newx = self.rect.x + self.change_x
            newy = self.rect.y + self.change_y
         
            #If our x value is within the bounds of the screen:
            if newx >= 0 and newx < x_limit - self.rect.width:
                self.rect.x = newx
            
            #If the x value isn't:

            elif newx < 0:
                self.rect.x = 0
            elif newx > x_limit - self.rect.width:
                self.rect.x = x_limit - self.rect.width
             
            #If our y value is within the bounds of the screen:
            if newy >= 0 and newy  < y_limit - self.rect.height:
                self.rect.y = newy
        
            #If the y value isn't:
            elif newy < 0:
                self.rect.y = 0.
            elif newy >= y_limit - self.rect.height:
                self.rect.y = y_limit - self.rect.height
            
            """Code block for maintaining walking frames""" 
            #(And the player's image layers)
                               
            if self.direction == "L":
                walking_frame = (self.rect.x // self.move_speed) % len(self.walking_frames_l)
                self.image = self.walking_frames_l[walking_frame]
                self.draw_first = False
            elif self.direction == "R":
                walking_frame = (self.rect.x // self.move_speed) % len(self.walking_frames_r)
                self.image = self.walking_frames_r[walking_frame]
                self.draw_first = True
            elif self.direction == "U":
                walking_frame = (self.rect.y // self.move_speed) % len(self.walking_frames_u)
                self.image = self.walking_frames_u[walking_frame]
                self.draw_first = False
            elif self.direction == "D":
                walking_frame = (self.rect.y // self.move_speed) % len(self.walking_frames_d)
                self.image = self.walking_frames_d[walking_frame]
                self.draw_first = True
                
            #Regardless of the image, we want it to be slightly smaller than the tile size, which happens to be 80 pixels
            self.image = pygame.transform.scale(self.image, [50, 70])
                
            #This code checks to see whether or not the player should be attacking
            if self.attacking and self.equipped_main_hand:
                self.attack(screen, frame)
                
        else:
            self.stop()
            
        """Code block for managing sprite collisions""" 
        """I don't think I'll need this code at all, but I'm going to keep it commented just in case"""
        
        """
        block_hit_list = pygame.sprite.spritecollide(self, self.room.obstacle_list, False)
        
        for block in block_hit_list:
            if self.direction == "L":
                self.rect.left = block.rect.right
                self.stop_left()
            elif self.direction == "R":
                self.rect.right = block.rect.left
                self.stop_right()
            elif self.direction == "U":
                self.rect.top = block.rect.bottom
                self.stop_up()
            elif self.direction == "D":
                self.rect.bottom = block.rect.top
                self.stop_down()
        """
                
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
            if self.frame == 19:
                print(self.attacking)
                self.equipped_main_hand.attacking = False
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
        
