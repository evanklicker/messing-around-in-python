import pygame

WHITE = (255, 255, 255)

class Shield():
    def __init__(self, player):
        
        
        self.image= pygame.image.load("./items/woodenshield.png").convert()
        
        self.image.set_colorkey(WHITE)
        
        #We need to set our item type, so we can know what we're supposed to do with this item
        #Remember, 1 is main hand, 2 is off hand, 3 is consumable, and 4 is other
        self.item_type = 2
        
        #Since this won't be animated nearly as much as a sword, we don't need nearly as many variables to draw it
        self.posx = 0
        self.posy = 0
        
        #These will be added to the player's stats, if the item is equipped
        self.defense = 2
        self.attack  = 0
        
    def draw(self, screen, pos):
		
		#If we later add some difference in what the player looks like based on the equipped shield
		#This method will be called only by the inventory class. Until then, it's used by both
        screen.blit(self.image, pos)
        
    def update(self, screen, player, frame):
		
        #Since we aren't really drawing it to the screen, there's nothing to update
        pass
