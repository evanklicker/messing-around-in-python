import pygame
import player as p
import quitter as q

BLACK = (  0,   0,   0)
BROWN = (130,  94,  35)
WHITE = (255, 255, 255)
GREEN = (  0, 255,   0)
RED   = (255,   0,   0)
BLUE  = (  0,   0, 255)
    
def main():
    
    pygame.init()
    
    WINDOW_SIZE = (800, 600)
    screen = pygame.display.set_mode(WINDOW_SIZE)
    
    pygame.display.set_caption("My Game")
    
    player = p.Player(screen)
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                
            #We're going to run two different event loops, to keep things organized
            #The first one is going to handle anything that happens during a paused moment
            #I'm putting it first because I think those screens should have priority, if any issues come up
            if game_state >= 1:  
                
                player.stop()
                
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_RETURN or event.key == pygame.K_i) and not quitter.quitting:
                        player.showing_inventory = False
                
                    if event.key == pygame.K_ESCAPE:
                        #If we're quitting, stop trying. If we aren't, start trying
                        quitter.quitting = not quitter.quitting
                                     
                #If the user clicked   
                if event.type == pygame.MOUSEBUTTONDOWN:
                
                    #Because we are almost certainly going to need it
                    pos = pygame.mouse.get_pos()
                
                    #And the click was a left click
                    if event.button == 1:
                        
                        #And they are considering quitting
                        if quitter.quitting:
                            #Check to see if they clicked a button
                            #See? We did need it
                            quitter.button_depress(screen, pos)
                        
                        #Or, if the inventory is showing
                        elif player.showing_inventory:
                            #Select an item
                            player.inventory.select_item(pos)                       
                        
                if event.type == pygame.MOUSEBUTTONUP:
                    done = quitter.quit_check(screen, pygame.mouse.get_pos())
                    
            #If there are no menus, or quit prompts, or anything showing, run normally
            elif game_state == 0:            
            
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.go_left()
                    if event.key == pygame.K_RIGHT:
                        player.go_right()
                    if event.key == pygame.K_UP:
                        player.go_up()
                    if event.key == pygame.K_DOWN:
                        player.go_down()
                    if event.key == pygame.K_SPACE or event.key == pygame.K_z:
                        player.attacking = True 
                    if event.key == pygame.K_RETURN or event.key == pygame.K_i:
                        player.showing_inventory = True      
                    if event.key == pygame.K_ESCAPE:
                        player.attacking = False
                        #Switch the state of quitter.quitting:
                        quitter.quitting = True  
                            
                if event.type == pygame.KEYUP:
                    if not quitter.quitting:
                        if event.key == pygame.K_LEFT:
                            player.stop_left()                
                        if event.key == pygame.K_RIGHT:
                            player.stop_right()
                        if event.key == pygame.K_UP:
                            player.stop_up()
                        if event.key == pygame.K_DOWN:
                            player.stop_down()            
                    if event.key == pygame.K_SPACE or event.key == pygame.K_z:
                        player.attacking = False
                        
            else:
                game_state = 0
                          
        player.update(screen, frame)
                
        screen.fill(WHITE)
        
        player.draw(screen, frame)
        
        if quitter.quitting:
            quitter.draw(screen)  
        
        frame += 1
        if frame > 20:
            frame = 0
            print("frames reset")
            
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
