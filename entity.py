import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, current_room):
        pygame.sprite.Sprite.__init__(self)
        
        #Possible directions are Left (L), Right (R), Up (U), Down (D)
        self.direction = "R"
        
        #Based on direction- determined in the update method
        self.draw_first = False
        
        #This will be false if the game is paused
        self.updating = False

        #Entity walking images
        self.walking_frames_u = []
        self.walking_frames_d = []
        self.walking_frames_l = []
        self.walking_frames_r = []
        
        #Which room are we in?
        self.room = current_room
        
        #Create our entity image
        self.get_image()
        
        #Align the walking frames, and get our position
        self.image = self.walking_frames_r[0]
        self.rect = self.image.get_rect()
        
        #Other misc movement attributes
        self.standing_frame = 0
        self.move_speed = 2
        self.moving = [False, False, False, False]
        
        #Grab the width measurement for the room's tiles
        self.walking_frame = self.room.tile_list[0][0].rect.width
        self.can_move = True
        
        #Attributes for attacking
        self.attack_cooldown = 20 #frames
        self.cooldown_done = True
        self.attacking = False
        self.frame = 0
        self.frame_temp = 0
        
        
    #Self explanatory
    def go_left(self):
        
        if self.can_move:
            self.direction = "L"
            #self.room.entity_left(self)
            self.can_move = self.room.entity_left(self)
        
        
    def go_right(self):
        
        if self.can_move:
            self.direction = "R"
            #self.room.entity_right(self)
            self.can_move = self.room.entity_right(self)
        
        
    def go_up(self):
        
        if self.can_move:
            self.direction = "U"
            #self.room.entity_up(self)
            self.can_move = self.room.entity_up(self)
        
        
    def go_down(self):
        
        if self.can_move:
            self.direction = "D"
            #self.room.entity_down(self)
            self.can_move = self.room.entity_down(self)
        
            
    def get_room_pos(self):
        
        for column in range(self.room.tile_list.__len__()):
            for row in range(self.room.tile_list[column].__len__()):
                if self.room.tile_list[column][row].contained_entity == self:
                    return [column, row]
        return [0, 0]
        
    '''      
    def collision_check(self):
        
        #Make a new entity
        future_entity = copy.copy(self)
        #And check to see if he would run into a wall
        #If he does, return True
        if self.direction == "L":
            future_entity.rect.x -= self.rect.width
            if pygame.sprite.spritecollide(future_entity, self.room.obstacle_list, False).__len__() > 0:
                return True
            else:
                return False
        
        elif self.direction == "R" :
            future_entity.rect.x += self.rect.width
            if pygame.sprite.spritecollide(future_entity, self.room.obstacle_list, False).__len__() > 0:
                return True
            else:
                return False
                
        elif self.direction == "U":
            future_entity.rect.y -= self.rect.width
            if pygame.sprite.spritecollide(future_entity, self.room.obstacle_list, False).__len__() > 0:
                return True
            else:
                return False                
        
        elif self.direction == "D":
            future_entity.rect.y += self.rect.width
            if pygame.sprite.spritecollide(future_entity, self.room.obstacle_list, False).__len__() > 0:
                return True
            else:
                return False
    '''        
        
    def update(self, screen, frame):
        
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
                self.standing_frame += 1
                
            if self.standing_frame >= self.image_frames.__len__():
                self.standing_frame = 0
            
            self.image = self.image_frames[self.standing_frame]
            
            if self.moving[0]:
                self.go_left()
            elif self.moving[1]:
                self.go_right()
            elif self.moving[2]:
                self.go_up()
            elif self.moving[3]:
                self.go_down()
            
            if not self.can_move:
                #Move_speed is at 2 so he moves a bit faster. It is hilarious to see it at 1, though
                self.walking_frame -= self.move_speed
                self.image = self.image_frames[-(self.walking_frame // 5 % self.image_frames.__len__())]
                if self.walking_frame <= 0:
                    #Grab any tile's width- specifically, the top-left tile. They're all the same, anyway
                    self.walking_frame = self.room.tile_list[0][0].rect.width
                    self.can_move = True
          
                
            #Regardless of the image, we want it to be slightly smaller than the tile size, which happens to be 80x80 pixels
            self.image = pygame.transform.scale(self.image, [50, 70])
            
    def get_image(self, image_path):
        #This loads and creates the walking frames to be used by the player
        
        sprite_sheet = ss.SpriteSheet(image_path)
      
        #image = sprite_sheet.get_image(x_start, y_start, width, height)
        #self.walking_frames_u.append(image)

 
