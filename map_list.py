#This is a list of every room to be used in the game

from map import *
import pygame
BLACK = (  0,   0,   0)

class Map1(Map):
    def __init__(self, screen):
        Map.__init__(self)
        
        self.tile_list  = []
        self.tile_group = pygame.sprite.Group()
        
        #A list to hold every tile's image, in order of appearance (left to right, then top to bottom)
        #To make creating the tiles much easier
        tile_images = []
        
        #Let's make it more fun than just a white background
        #This makes the top row of Tiles the same picture (brick)
        edge_image = pygame.image.load("./environment/basic_tileset/stone_brick_tile.png").convert()
        for i in range(10):
            tile_images.append(edge_image)
            
        #This makes the first and last tile of each row the same (brick), and everything in between something else (grass)
        body_image = pygame.image.load("./environment/basic_tileset/grass_tile.png").convert()
        for i in range(13):
            
            #Add the brick for the top
            tile_images.append(edge_image)
            
            for j in range(8):
                #Add the grass for the middle
                tile_images.append(body_image)
                
            #Add the brick for the bottom
            tile_images.append(edge_image)
            
        #This finishes out the last row with the first image (brick)
        for i in range(10):
            tile_images.append(edge_image)
        #We're going to create a nested array to hold every tile, to make indexing easier
        nested_part = []
                    
        #Fill the screen with tiles
        index = 0
        for column in range(15):
            
            #Refresh the nested part of the list
            nested_part = []
            for row in range(10):
                
                #Get the next image and create the tile
                image = tile_images[index]
                tile = Tile(screen, column, row, image)
                
                #If we aren't supposed to be able to walk through the tile, set it as an obstacle
                if image == edge_image:
                    tile.is_obstacle = True
                    
                #Put the tile in the sprite Group
                self.tile_group.add(tile)
                
                #And put the tile in the nested part of the list
                nested_part.append(tile)
                
                #Increase index
                index += 1
                
            #When the inner loop is finished, we add the nested part of the list to the main list    
            self.tile_list.append(nested_part)
            
