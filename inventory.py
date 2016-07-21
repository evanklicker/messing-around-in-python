import pygame

GREEN = (  0, 255,   0)
GREY  = ( 50,  50,  50)

class Inventory():
    def __init__(self, screen):
        
        #So we can check for collisions without having to check pixel groups individually
        self.slot_list = []
        
        #So we can alias with the player's inventory easier
        self.item_list = []
        
        #The distance between inventory slots
        self.margin = 20
        
        #Whether or not an inventory slot is selected
        self.has_selected = False
        
        #Adding inventory slots- 8 of 'em
        for i in range(8):
            
            #Create some brand-new slots
            
            #For the left column
            if i < 4:
                slot = Slot(0, i)
                
            #For the right column
            else:
                slot = Slot(1, i - 4)
            self.slot_list.append(slot)
            
        """The next part has some fancy and convoluted math that isn't done, so beware"""
            
        #This is the distance between the egde of the screen and the edge of the inventory slot
        #This should never need to be rounded, unless the margin or screen width somehow become odd
        self.x_offset = round(screen.get_size()[0] - ((screen.get_size()[0] + self.margin) / 2))
        
        #I multiplied this by 1.2 because I wanted it to be a little uneven- more buffer at the top than at the bottom
        self.y_offset = slot.rect.height + self.margin * 4
    
        for slot in self.slot_list:
            #This will just be self.x_offset for row 1, and then a bit to the right for row 2
            slot.rect.x = self.x_offset + slot.row_position * (slot.rect.width + self.margin) - slot.rect.width
            
            #Similarly, this will just be self.y_offset for column 1, and then shift down accordingly for the rest
            slot.rect.y = self.y_offset + slot.column_position * (slot.rect.height + self.margin) - slot.rect.height
            
        #Now that we've made the storage slots, we should make two more slots- one to hold the main-hand item, and one to hold the off-hand item
        #This is for the main-hand slot
        slot = Slot(5, 5)
        slot.rect.x = 100
        slot.rect.y = 100
        self.slot_list.append(slot)
        
        #This is for the off-hand slot
        slot = Slot(6, 6)
        slot.rect.x = screen.get_size()[0] - 210
        slot.rect.y = 100
        self.slot_list.append(slot)
    
    def draw(self, screen):
        
        for slot in self.slot_list:
            slot.draw(screen)
          
    #This function will put an item that's stored in the normal inventory slots and put it into the correct main or off-hand slots, or consume it          
    def equip_item(self, mouse_pos):
        for slot in self.slot_list:
            if slot.selected:
                
                #If you clicked the main-hand item slot and the selected item can go there
                if self.slot_list[8].rect.collidepoint(mouse_pos) and slot.contained_item.item_type == 1:
                    if self.unequip_main():
                        self.slot_list[8].contained_item = slot.contained_item
                        slot.contained_item = None
                
                #Or, if you clicked the off-hand item slot and the selected item can go there
                elif self.slot_list[9].rect.collidepoint(mouse_pos) and slot.contained_item.item_type == 2:
                    if self.unequip_off():
                        self.slot_list[9].contained_item = slot.contained_item
                        slot.contained_item = None
                    
                #Lastly, if you clicked the same item slot and the selected item is consumable    
                elif slot.rect.collidepoint(mouse_pos) and slot.contained_item.item_type == 3:
                    if slot.contained_item.consume():
                        self.lose_item(slot.contained_item)
                    
    #Remove any item that's currently in the main-hand slot                                    
    def unequip_main(self):
        #First things first: Is there even an item to remove?
        if self.slot_list[8]:
            #If we have space in our inventory
            if len(self.item_list) < 8:               
                #Will be true if there was an item, it was lost, and then successfully put back into the inventory
                return self.get_item(self.lose_item(self.slot_list[8].contained_item))
            else:
                return False
        return True
        
    #Remove any item that's currently in the off-hand slot
    def unequip_off(self):
        #Same as the previous function: Is there anything to remove?
        if self.slot_list[9].contained_item:
            #If we have space in our inventory
            if len(self.item_list) < 8:
                return self.get_item(self.lose_item(self.slot_list[9].contained_item))
            else:
                return False
        return True
        
    #Prepare items to be used
    def select_item(self, mouse_pos):
        if self.has_selected:
            self.equip_item(mouse_pos)
            self.deselect_items()
        else:
            self.deselect_items()
            for slot in self.slot_list:
                if slot.rect.collidepoint(mouse_pos) and slot.contained_item:
                    slot.selected = True
                    self.has_selected = True
             
    #Self explanatory   
    def deselect_items(self):
        for slot in self.slot_list:
            slot.selected = False
            self.has_selected = False
            
    def get_item(self, item):
        #I used "i in range" instead of "slot in self.slot_list" because the main-hand and off-hand slots are part of the slot list
        #And I don't want items to go to those slots unless the player specifically wants it to happen
        for i in range(8):
            if not self.slot_list[i].contained_item:
                self.slot_list[i].get_item(item)
                self.item_list.append(item)
                return True
        return False
           
    #Get rid of any item     
    def lose_item(self, item):
        if item in self.item_list: 
            self.item_list.remove(item)
        for slot in self.slot_list:
            if slot.lose_item(item):
                return item
        return None
    
    #Returns the index value of an item           
    def find_item(self, item):
        index = 0
        for slot in self.slot_list:
            if slot.contained_item == item:
                return index
            else:
                index += 1    
        return None        
            
            
    """This class is used only in the inventory class, and only to contain items"""
        
class Slot(pygame.sprite.Sprite):
    def __init__(self, row_position, column_position):
        super().__init__()
        
        #It's just a white image
        Slot.image = pygame.image.load("./items/inventory_slot_background.png")
        
        #This attribute holds the contained item's image, if it exists
        self.image_overlay = None
        
        #Does this slot have an item? Is the slot selected?
        self.contained_item = None
        self.selected = False
        
        self.row_position = row_position
        self.column_position = column_position
        
        self.rect = self.image.get_rect()
        
        self.selection_bracket_length = 20
        self.selection_bracket_height = 70
        
    def draw(self, screen):
    
        pygame.draw.rect(screen, GREY, [self.rect.x - 5, self.rect.y - 5, self.rect.width + 10, self.rect.height + 10])
        screen.blit(self.image, self)
        if self.contained_item:
            self.contained_item.draw(screen, [self.rect.x + (self.rect.width - self.contained_item.image.get_rect().width) / 2, self.rect.y + (self.rect.height - self.contained_item.image.get_rect().height) / 2])
      
        if self.selected:
            #Left Bracket
            #Horizontal Line
            pygame.draw.line(screen, GREEN, 
            [self.rect.x + 10, self.rect.y + 10], [self.rect.x + 30, self.rect.y + 10])
            
            #Verticle Line
            pygame.draw.line(screen, GREEN, 
            [self.rect.x + 10, self.rect.y + 10], [self.rect.x + 10, self.rect.y + 90])
            
            #Horizontal Line
            pygame.draw.line(screen, GREEN, 
            [self.rect.x + 10, self.rect.y + 90], [self.rect.x + 30, self.rect.y + 90])
                    
            #Right Bracket
            #Horizontal Line
            pygame.draw.line(screen, GREEN, 
            [self.rect.x + 70, self.rect.y + 10], [self.rect.x + 90, self.rect.y + 10])
            
            #Verticle Line
            pygame.draw.line(screen, GREEN, 
            [self.rect.x + 90, self.rect.y + 10], [self.rect.x + 90, self.rect.y + 90])
            
            #Horizontal Line
            pygame.draw.line(screen, GREEN, 
            [self.rect.x + 70, self.rect.y + 90], [self.rect.x + 90, self.rect.y + 90])
                                                    
    def get_item(self, item):
        if not self.contained_item and item:
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
            
