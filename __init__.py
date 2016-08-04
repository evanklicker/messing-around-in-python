import pygame, player as p, quitter as q, 

def init():
	
	pygame.init()
    
    WINDOW_SIZE = (1200, 800)
    screen = pygame.display.set_mode(WINDOW_SIZE)
    
    pygame.display.set_caption("My Game")
    pygame.key.set_repeat(0)
    
    room_list = []
    
    room = m.Map1(screen)
    room_list.append(room)
    
    current_room = room_list[0]   
    
    player = p.Player(screen, current_room)
    quitter = q.Quit_box(screen)
    
    current_room.tile_list[5][5].get_entity(player)
    
    done = False
    
    frame = 0
    
    #If game_state = 0, the game should run like normal (This is what we're starting with)
    #Anything more than 0, and the game should be paused
    #game_state = 1 means the quit prompt is showing
    #game_state = 2 means the player's inventory is showing
    game_state = 0
    
    clock = pygame.time.Clock()
 
