

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
        
        #Grab the width measurement for the room's tiles
        self.walking_frame = self.room.tile_list[0][0].rect.width
        self.can_move = True
        
        #Attributes for attacking
        self.attack_cooldown = 20 #frames
        self.cooldown_done = True
        self.attacking = False
        self.frame = 0
        self.frame_temp = 0
 
