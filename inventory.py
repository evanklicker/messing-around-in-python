import pygame

class Inventory():
    def __init__(self, screen):
        
        #So we can check for collisions without having to check pixel groups individually
        self.slot_list = pygame.sprite.Group()
        
        #So we can alias with the player's inventory easier
        self.item_list = []
        
        #The distance between inventory slots
        self.margin = 20
        
        #Adding inventory slots- 8 of 'em
        for i in range(8):
            
            #Create some brand-new slots
            #For the left column
            if i < 4:
                slot = Slot(0, i)
            #For the right column
            else:
                slot = Slot(1, i - 4)
            self.slot_list.add(slot)
            
        #This is the distance between the egde of the screen and the edge of the inventory slot
        #This should never need to be rounded, unless the margin or screen width somehow become odd
        self.x_offset = round(screen.get_size()[0] - ((screen.get_size()[0] + self.margin) / 2))
        
        #I multiplied this by 1.2 because I wanted it to be a little uneven- more buffer at the top than at the bottom
        self.y_offset = slot.image_rect.height + self.margin * 4
    
            
        for slot in self.slot_list:
            #This will just be self.x_offset for row 1, and then a bit to the right for row 2
            slot.rect[0] = self.x_offset + slot.row_position * (slot.image_rect.width + self.margin) - slot.image_rect.width
            print("X_offset = ", self.x_offset)
            print("Slot.row_position = ", slot.row_position)
            print("Slot.image_rect.width = ", slot.image_rect.width)
            print("Margin = ", self.margin)
            print(slot.rect[0])
            
            #Similarly, this will just be self.y_offset for column 1, and then shift down accordingly for the rest
            slot.rect[1] = self.y_offset + slot.column_position * (slot.image_rect.height + self.margin) - slot.image_rect.height
            print(slot.rect[1])
    
    def draw(self, screen):
        
        for slot in self.slot_list:
            
            slot.draw(screen)
                
        #print("Inventory Drawn!")
        
    def select_item(self, mouse_pos):
        self.deselect_items()
        for slot in self.slot_list:
            if slot.rect.collidepoint(mouse_pos):
                slot.selected = True
                
    def deselect_items(self):
        for slot in self.slot_list:
            slot.selected = False
            
    def get_item(self, item):
        for slot in self.slot_list:
            if not slot.contained_item:
                slot.get_item(item)
                self.item_list.append(item)
                return True
                
    def lose_item(self, item):
        for slot in self.slot_list:
            slot.lose_item(item)
        self.item_list.remove(item)
                
    def find_item(self, item):
        index = 0
        for slot in self.slot_list:
            if slot.contained_item == item:
                return index
            else:
                index += 1			
            
            
    """This class is used only in the inventory class, and only to contain items"""
	    
class Slot(pygame.sprite.Sprite):
    def __init__(self, row_position, column_position):
        super().__init__()
        
        #It's just a white image
        Slot.image = pygame.image.load("./Items/inventory_slot_background.png")
        
        self.image_overlay = None
        
        Slot.image_rect = self.image.get_rect()

        self.contained_item = None
        self.selected = False
        
        self.row_position = row_position
        self.column_position = column_position
        
        self.rect = self.image.get_rect()
        
        self.selection_bracket_length = 20
        self.selection_bracket_height = 70
        
    def draw(self, screen):
		
        screen.blit(self.image, self)
        if self.contained_item:
            self.contained_item.draw(screen, [self.rect[0] + 25, self.rect[1] + 25])
      
        if self.selected:
            #Left Bracket
            #Horizontal Line
            pygame.draw.line(screen, GREEN, 
            [posx + 20, posy + 20], [self.rect[0] + 40, self.rect[1] + 20])
            
            #Verticle Line
            pygame.draw.line(screen, GREEN, 
            [posx + 20, posy + 20], [self.rect[0] + 20, self.rect[1] + 80])
            
            #Horizontal Line
            pygame.draw.line(screen, GREEN, 
            [posx + 20, posy + 80], [self.rect[0] + 40, self.rect[1] + 80])
                    
            #Right Bracket
            #Horizontal Line
            pygame.draw.line(screen, GREEN, 
            [posx + 60, posy + 20], [self.rect[0] + 80, self.rect[1] + 20])
            
            #Verticle Line
            pygame.draw.line(screen, GREEN, 
            [posx + 80, posy + 20], [self.rect[0] + 80, self.rect[1] + 80])
            
            #Horizontal Line
            pygame.draw.line(screen, GREEN, 
            [posx + 60, posy + 80], [self.rect[0] + 80, self.rect[1] + 80])
                                                    
    def get_item(self, item):
        if not self.contained_item:
            self.contained_item = item  
            self.image_overlay = item.image                                                 
            return item
             
        else:
            return None
             
    def lose_item(self, item):
        if self.contained_item == item:
            self.contained_item = None
            return item
            
        else:
            return None
            
