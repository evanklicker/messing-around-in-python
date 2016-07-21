import pygame

class Map():
    def __init__(self):
        
        #The enemy_list variable stores enemy objects, but it doesn't need to worry about their positions
        #Like this: [enemy1, enemy2, ...]
        self.enemy_list = []
        
        #The obstacle_list variable stores obstacles that can't be walked through
        #It stores them like this: [obstacle_object1, obstacle_object2]
        self.obstacle_list = pygame.sprite.Group()
        
        #This list stores obstacles that can be walked through
        self.non_obstacle_list = []
        
        #A list for every tile in the room
        self.tile_list = pygame.sprite.Group()
        
class Tile(pygame.sprite.Sprite):
    def __init__(self, screen, column_number = 0, row_number = 0, image = None, image_path = "./items/inventory_slot_background.png"):
        pygame.sprite.Sprite.__init__(self)
        #default the image to white if no image was given, for some reason
        if image:
            self.image = image
        else:
            self.image = pygame.image.load(image_path)
        
        #The usual
        self.rect = self.image.get_rect()
        
        #Make every tile the same size- the right size so there is a 15x10 grid
        x, y = screen.get_size()
        
        if self.rect.width != x // 15 or self.rect.height != y // 10:
            self.image = pygame.transform.scale(self.image, [x // 15, y // 10])
            self.rect = self.image.get_rect()
        
        #These will be used to determine the position of the tile
        self.column_number = column_number
        self.row_number = row_number
        
        self.rect.x = self.column_number * self.rect.width
        self.rect.y = self.row_number * self.rect.height
        
        #Is somebody occupying this square? Not by default
        self.contained_entity = None
        
    def draw(self, screen):
        
        screen.blit(self.image, [self.rect.x, self.rect.y])
        
        #Draw the contained entity, but do it in the middle of the square, instead of the top left
        if self.contained_entity:
            self.contained_entity.draw(screen, (self.rect.width - self.contained_entity.rect.width / 2), (self.rect.height - self.contained_entity.rect.height / 2))
        
    def update(self, screen, frame):
        
        #We only need to update if we have a creature to update
        if self.contained_entity:
            self.contained_entity.update(screen, frame)
        
    def get_entity(self, entity):
        
        self.contained_entity = entity
        
    def lose_entity(self):
        
        self.contained_entity = None
