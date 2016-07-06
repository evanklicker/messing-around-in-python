import pygame

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)

class SpriteSheet(object):
    def __init__(self, filename):
        self.sprite_sheet = pygame.image.load(filename)
    
    def get_image(self, x, y, width, height):
        image = pygame.Surface([width, height])
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(BLACK)
        return image
