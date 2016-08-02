import pygame
import queue

def handle_events(player, quitter, screen, game_state=0, done=False):
    """
    This method should be called from the main loop. Unless it's called manually somewhere else,
    the game_state variable will always be supplied.
    
    :param player: Should be supplied by the main loop. Required, and this will fail without it
    :type  player: player.Player object
    
    :param quitter: Also needs to be supplied for the method to work. I will try to cut this out in future updates
    :type quitter: quitter.Quitter object
    
    :param screen: The surface that things (quit screen, player) will be drawn to
    :type screen: pygame.Surface object
    
    :param game_state: Determines which part of the event handling loop that will be accessed.
        If the number is zero, the game will run noramlly. If it is greater than 0, it will be paused.
        0 --> Normal
        1 --> The player's inventory is showing
        2 --> The quit menu is being displayed
    :type game_state: int
    
    :param done: If this is true, then the whole program will exit. If we are done, then quit
    :type done: boolean
    
    """ 
    
    for important_event in pygame.event.get():
        if important_event.type == pygame.QUIT:
            done = True
                
        #I'm going to run two different event loops, to keep things organized
        #If 'game_state' is greater than one, the loop is going to handle anything that happens during a paused moment
        #I'm putting it first because I think those screens should have priority, if any issues come up
        
        #If the user clicked   
        if important_event.type == pygame.MOUSEBUTTONDOWN:
                
            #Because we are almost certainly going to need it
            pos = pygame.mouse.get_pos()
               
            #And the click was a left click
            if important_event.button == 1:
                        
                #And they are considering quitting
                if quitter.quitting:
                    #Check to see if they clicked a button
                    #See? We did need it
                    quitter.button_depress(screen, pos)
                        
                #Or, if the inventory is showing
                elif player.showing_inventory:
                    #Select an item
                    player.inventory.select_item(pos)                       
                        
        if important_event.type == pygame.MOUSEBUTTONUP:
            done = quitter.quit_check(screen, pygame.mouse.get_pos())
            
        pygame.event.pump()
     
        event = pygame.key.get_pressed()  
            
        if game_state >= 1:  
                
            player.updating = False
                
            if event[pygame.K_RETURN] or event[pygame.K_i] and not quitter.quitting:
                player.showing_inventory = False
                   
            if event[pygame.K_ESCAPE]:
                #If we're quitting, stop trying. If we aren't, start trying
                quitter.quitting = not quitter.quitting
                   
        #If there are no menus, or quit prompts, or anything showing, run normally
        elif game_state == 0:  
                
            player.updating = True          
            
            if event[pygame.K_LEFT]:
                player.go_left()
                    
            if event[pygame.K_RIGHT]:
                player.go_right()
                    
            if event[pygame.K_UP]:
                player.go_up()
                
            if event[pygame.K_DOWN]:
                player.go_down()
                
            if event[pygame.K_SPACE] or event[pygame.K_z]:
                #If "SPACE" or "Z" is pressed, attack!
                player.attacking = True 
                    
            if event[pygame.K_RETURN] or event[pygame.K_i]:
                #If "Enter" or "I" is pressed, bring up the inventory
                player.showing_inventory = True   
                       
            if event[pygame.K_ESCAPE]:
                #Switch the state of quitter.quitting to true
                quitter.quitting = True  
                                    
        else:
            #This shouldn't ever happen. But if it does, I'm ready
            game_state = 0
                
    return game_state, done
