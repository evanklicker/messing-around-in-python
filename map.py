import pygame

BLACK = (  0,   0,   0)

class Map():
    def __init__(self):
        
        #The enemy_list variable stores enemy objects, but it doesn't need to worry about their positions
        #Like this: [enemy1, enemy2, ...]
        self.enemy_list = []
       
        #A list for every tile in the room
        self.tile_list = pygame.sprite.Group()
        
    def collision_check(self, entity, direction):
        
        x, y = entity.get_room_pos()
        
        if direction == "L":
            if self.tile_list[x - 1][y].is_obstacle:
                return False
            else:
                return True
                
        elif direction == "R":
            if self.tile_list[x + 1][y].is_obstacle:
                return False
            else:
                return True
                
        elif direction == "U":
            if self.tile_list[x][y - 1].is_obstacle:
                return False
            else:
                return True        
        
        elif direction == "D":
            if self.tile_list[x][y + 1].is_obstacle:
                return False
            else:
                return True   
                
    def entity_left(self, entity):
        
        for column in range(self.tile_list.__len__()):
            for row in range(self.tile_list[column].__len__()):
                if self.tile_list[column][row].contained_entity == entity and self.collision_check(entity, "L"):
                    self.tile_list[column][row].lose_entity()
                    self.tile_list[column - 1][row].get_entity(entity)
        
            
    def entity_right(self, entity):
		
        for column in range(self.tile_list.__len__()):
            for row in range(self.tile_list[column].__len__()):
                if self.tile_list[column][row].contained_entity == entity and self.collision_check(entity, "R"):
                    self.tile_list[column][row].lose_entity()
                    self.tile_list[column + 1][row].get_entity(entity)
                
    def entity_up(self, entity):
		
        for column in range(self.tile_list.__len__()):
            for row in range(self.tile_list[column].__len__()):
                if self.tile_list[column][row].contained_entity == entity and self.collision_check(entity, "U"):
                    self.tile_list[column][row].lose_entity()
                    self.tile_list[column][row - 1].get_entity(entity)
        
    def entity_down(self, entity):           
		 
        for column in range(self.tile_list.__len__()):
            for row in range(self.tile_list[column].__len__()):
                if self.tile_list[column][row].contained_entity == entity and self.collision_check(entity, "D"):
                    self.tile_list[column][row].lose_entity()
                    self.tile_list[column][row + 1].get_entity(entity)                
    
    def draw(self, screen):
        
        """
        NOTE: I could have written this draw method two different ways.
        The way I did it, I loop through every tile and call its tile.draw() method.
        I could have just called self.tile_group.draw(), and that would have put everything on the scree,
        but it wouldn't put any entities on the screen. I'd have to loop through the tiles and draw things either way
        """
        
        black = pygame.image.load("./environment/black.png")

        #This should draw all the tiles, as well as the player and enemies
        for tiles in self.tile_list:
            for tile in tiles:
                tile.draw(screen)
                pygame.draw.line(screen, BLACK, [tile.rect.x, tile.rect.y], [tile.rect.x + tile.rect.width, tile.rect.y])
                pygame.draw.line(screen, BLACK, [tile.rect.x, tile.rect.y], [tile.rect.x, tile.rect.y + tile.rect.height])
                if tile.is_obstacle:
                    tile.image = black
                
        
    def update(self, screen, frame):
        
        #Update the tile group
        #This will call the player's update method, as well as every other entity's, through the grapevine.
        #But only after I make the movement constricted to tiles. For now, this update method won't do anything
        #Same things as before- I could call self.tile_group.update() and loop, or just loop through the tile list.
        for tiles in self.tile_list:
            for tile in tiles:
                tile.update(screen, frame)

        
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
        
        #If the tile can be walked through, this will be false
        self.is_obstacle = False
        
    def draw(self, screen):
        
        screen.blit(self.image, [self.rect.x, self.rect.y])
        
        #Draw the contained entity, but do it in the middle of the square, instead of the top left
        if self.contained_entity:
            self.contained_entity.draw(screen, (self.rect.width - self.contained_entity.rect.width / 2), (self.rect.height - self.contained_entity.rect.height / 2))

        
    def update(self, screen, frame):
        
        #We only need to update if we have a creature to update
        if self.contained_entity:
            self.contained_entity.rect.x = self.rect.x - (self.rect.width - self.contained_entity.rect.width) / 2
            self.contained_entity.rect.y = self.rect.y - (self.rect.height - self.contained_entity.rect.height) / 2
            self.contained_entity.update(screen, frame)
        
    def get_entity(self, entity):
        
        self.contained_entity = entity
        
    def lose_entity(self):
        
        self.contained_entity = None
