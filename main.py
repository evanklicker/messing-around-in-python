import pygame
import random
import player as p
import quitter as q
import map_list as m
from event_handler import *

BLACK = (  0,   0,   0)
BROWN = (130,  94,  35)
WHITE = (255, 255, 255)
GREEN = (  0, 255,   0)
RED   = (255,   0,   0)
BLUE  = (  0,   0, 255)
    
def main():
    
    pygame.init()
    
    WINDOW_SIZE = (1200, 800)
    screen = pygame.display.set_mode(WINDOW_SIZE)
    
    pygame.display.set_caption("My Game")
    
    room_list = []
    
    room = m.Map1(screen)
    room_list.append(room)
    
    current_room = room_list[0]    
    
    player = p.Player(screen, current_room)
    quitter = q.Quit_box(screen)
    
    done = False
    
    frame = 0
    
    #If game_state = 0, the game should run like normal (This is what we're starting with)
    #Anything more than 0, and the game should be paused
    #game_state = 1 means the quit prompt is showing
    #game_state = 2 means the player's inventory is showing
    game_state = 0
    
    clock = pygame.time.Clock()
    
    while not done:
        game_state, done = handle_events(player, quitter, screen, game_state)
                          
        #player.update(screen, frame)
        current_room.update(screen, frame)
                
        screen.fill(WHITE)
        
        current_room.draw(screen)
        player.draw(screen)
        
        if quitter.quitting:
            quitter.draw(screen)  
    
    
        index_x = random.randint(0, 14)
        index_y = random.randint(0, 9)
        current_room.tile_list[index_x][index_y].get_entity(player)
        
        frame += 1
        if frame > 20:
            frame = 0
            
        if player.showing_inventory:
            game_state = 1
            if quitter.quitting:
                game_state = 2
        
        elif quitter.quitting:
            game_state = 2
            
        else:
            game_state = 0
               
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    
        
if __name__ == "__main__":
    main()
