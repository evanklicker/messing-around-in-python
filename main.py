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
    
    window_size = (800, 600)
    screen = pygame.display.set_mode(window_size)
    
    pygame.display.set_caption("My Game")
    
    player = p.Player()
    quitter = q.quit_box(screen)
   
    done = False
    about_to_quit = False
    
    animation = False
    frame = 0
    frame_on = False
    
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
                #And the click was a left click
                if event.button == 1:
                    #And they are considering quitting
                    if quitter.quitting:
                        #Check to see if they clicked a button
                        quitter.button_depress(screen, pygame.mouse.get_pos())
                        
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

                #I arbitrarily decided to put this in the KEYUP section instead of the KEYDOWN section
                if event.key == pygame.K_ESCAPE:
                    player.attacking = False
                    #Switch the state of quitter.quitting:
                    if not quitter.quitting:
                        quitter.quitting = True
                    elif quitter.quitting:
                        quitter.quitting = False
                        
                                   
        player.update(screen, frame)
                
        screen.fill(WHITE)
         
        player.draw(screen, frame)
        
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
