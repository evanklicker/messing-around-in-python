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
    
    clock = pygame.time.Clock()
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                
            if event.type == pygame.KEYDOWN and not quitter.quitting:
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
                                     
            #If the user clicked   
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                #Because we are almost certainly going to need it
                pos = pygame.mouse.get_pos()
                
                #And the click was a left click
                if event.button == 1:
                    
                    #And they are considering quitting
                    if quitter.quitting:
                        #Check to see if they clicked a button
                        quitter.button_depress(screen, pos)
                    
                    #Or, if the inventory is showing
                    elif player.showing_inventory:
                        #Select an item
                        player.inventory.select_item(pos)
                        
                        
                        
                        
            if event.type == pygame.MOUSEBUTTONUP:
                done = quitter.quit_check(screen, pygame.mouse.get_pos())
                            
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
                    if event.key == pygame.K_RETURN or event.key == pygame.K_i:
                        player.showing_inventory = not player.showing_inventory
                        print(player.showing_inventory)

                #I arbitrarily decided to put this in the KEYUP section instead of the KEYDOWN section
                if event.key == pygame.K_ESCAPE:
                    player.attacking = False
                    #Switch the state of quitter.quitting:
                    quitter.quitting = not quitter.quitting
                        
                                   
        player.update(screen, frame)
                
        screen.fill(WHITE)
        
        player.draw(screen, frame)
        
        #screen.blit(pygame.image.load("./Items/inventory_slot_background.png"), [100, 100])
        
        if quitter.quitting:
            quitter.draw(screen)  
             
        pygame.display.flip()
        clock.tick(60)
        
        frame += 1
        if frame > 20:
            frame = 0
    
    pygame.quit()
    
        
if __name__ == "__main__":
    main()
