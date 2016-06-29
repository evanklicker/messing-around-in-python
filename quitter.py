import pygame

LIGHT_GREY = (180, 180, 180)
DARK_GREY  = ( 80,  80,  80)
BLACK      = (  0,   0,   0)
WHITE      = (255, 255, 255)

class Quit_box():
    def __init__(self, screen):
        
        #Are we considering quitting?
        self.quitting = False
        
        #Getting the screen to create the quit box with
        width, height = screen.get_size()
        
        #Outer box dimensions
        self.width = round(width / 3)
        self.height = round(height / 5)
        
        #Set the width of every border
        self.border_width = 4
        
        #Outer box starting position
        self.start_posx = (width  - self.width)  / 2
        self.start_posy = (height - self.height) / 2
        
        #The colors of the boxes
        #color1 is for the outer box
        #color2 is for the buttons
        self.color1 = LIGHT_GREY
        self.color2 = DARK_GREY
        
        #The "yes" and "no" button dimensions
        self.button_height = round(self.height / 5)
        self.button_width  = round(self.width  / 3)
        
        #The text features to be used in this class
        self.font = pygame.font.SysFont("Calibri", round(self.button_height * 0.8), True, False) 
        
        #The text to ask if the user is sure
        self.quit_text = self.font.render("Are you sure you want to quit?", True, BLACK)
        
        #The text for the "yes" and "no" boxes
        self.yes_text = self.font.render("Yes", True, BLACK)
        self.no_text  = self.font.render("No",  True, BLACK)
        
        #The distance between the edge of the outer box and the buttons
        self.button_x_offset = (self.width  * 2 / self.button_width) * 5
        
        #The x positions for the buttons
        self.yes_button_posx = self.start_posx + self.button_x_offset
        self.no_button_posx  = self.start_posx + self.width - (self.button_width + self.button_x_offset)
        
        #The y position for the buttons
        self.button_posy = (height + self.button_height) / 2
        
        #The state of each button
        self.yes_button_depress = False
        self.no_button_depress  = False
        
    def draw(self, screen):
        
        #For the outer box
        #REMINDER: CHANGE THE 15 AND 20 TO BE DEPENDANT VARIABLES
        pygame.draw.rect(screen, self.color1, [self.start_posx, self.start_posy, self.width, self.height])
        screen.blit(self.quit_text, [self.start_posx + 15, self.start_posy + 20])
        
        #For the outer box's border
        pygame.draw.rect(screen, self.color2, [self.start_posx - self.border_width, self.start_posy - self.border_width, 
        self.width + (self.border_width * 2), self.height + (self.border_width * 2)], self.border_width)
        
        #For the "yes" button
        #Same thing as before- Mathematically find a way to determine that '5' value based on font size
        pygame.draw.rect(screen, self.color2, 
        [self.yes_button_posx, self.button_posy, self.button_width, self.button_height], self.border_width)
        screen.blit(self.yes_text, [self.yes_button_posx + (self.button_width / 3), self.button_posy + 5])
        
        #The "animation" of the button being pressed
        if self.yes_button_depress:
            pygame.draw.rect(screen, WHITE, [self.yes_button_posx + self.border_width, self.button_posy + self.border_width, 
            self.button_width - (2 * self.border_width), self.button_height - (2 * self.border_width)], self.border_width)
             
        #For the "no" button
        #Same as "yes" button- font size
        pygame.draw.rect(screen, self.color2, 
        [self.no_button_posx, self.button_posy, self.button_width, self.button_height], self.border_width)
        screen.blit(self.no_text, [self.no_button_posx + (self.button_width / 3), self.button_posy + 5])
        
        #The "animation" of the button being pressed
        if self.no_button_depress:
            pygame.draw.rect(screen, WHITE, [self.no_button_posx + self.border_width, self.button_posy + self.border_width, 
            self.button_width - (2 * self.border_width), self.button_height - (2 * self.border_width)], self.border_width)
    
    def quit_check(self, screen, mouse_pos):
        
        #If the click was within the bounds of the "yes" button:
        #Since this is called when the left mouse button is lifted, not pressed, we also want to check and see if we started the click on the button with the self.no/yes_button_depress check
        if  mouse_pos[0] > (self.yes_button_posx) and mouse_pos[0] < (self.yes_button_posx + self.button_width) and mouse_pos[1] > (self.button_posy) and mouse_pos[1] < (self.button_posy + self.button_height) and self.yes_button_depress:
            return True
        
        #Or, if the click was within the bounds of the "no" button:    
        elif mouse_pos[0] > (self.no_button_posx) and mouse_pos[0] < (self.no_button_posx + self.button_width) and mouse_pos[1] > (self.button_posy) and mouse_pos[1] < (self.button_posy + self.button_height) and self.no_button_depress:
            self.quitting = False
            self.no_button_depress = False
            return False
                        
        #Otherwise, just do nothing, and reset the click states:
        else:
            self.yes_button_depress = False
            self.no_button_depress  = False
            return False
            
    def button_depress(self, screen, mouse_pos):
        """Check the pressing of a button separately from the function of the button press"""
        """This will also allow the user to click a button, then move the mouse off the button, and de-click, and have nothing happen"""
        
        #For the "yes" button
        if mouse_pos[0] > (self.yes_button_posx) and mouse_pos[0] < (self.yes_button_posx + self.button_width) and mouse_pos[1] > (self.button_posy) and mouse_pos[1] < (self.button_posy + self.button_height):
            self.yes_button_depress = True
        
        #For the "no" button
        if mouse_pos[0] > (self.no_button_posx) and mouse_pos[0] < (self.no_button_posx + self.button_width) and mouse_pos[1] > (self.button_posy) and mouse_pos[1] < (self.button_posy + self.button_height):
            self.no_button_depress = True
