import pygame as pg
from states import Game

pg.init()

white = pg.Color(255, 255, 255)
black = pg.Color(0, 0, 0)
background = (43, 135, 209)
logo = pg.image.load("images/logo.png")

size = (400, 310)
FPS = 60
screen = pg.display.set_mode(size)
pg.display.set_caption("Memoria")
pg.display.set_icon(logo)
clock = pg.time.Clock()



def main():
    game = Game()
    
    while game.vs["run"]:
        mouse_pos = pg.math.Vector2(pg.mouse.get_pos())
        time_now = pg.time.get_ticks()
        
        # ----------- Event-Handler -------------#
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game.vs["run"] = False
                
            elif event.type == pg.MOUSEBUTTONDOWN:
                game.event_handler(game.vs["state"], game, mouse_pos, time_now)
                
        # ----------- Logica -------------#
        
        game.update(game.vs["state"])
        game.animar(time_now)
        
        # ----------- Dibujado -------------#
        
        screen.fill(background)
        game.draw(screen, game.vs["state"])
                  
        # ----------- Frame-Act -------------#
        
        clock.tick(FPS)
        pg.display.flip()
        
    if game.vs["retry"]:
        main()
        
if __name__ == "__main__":
    main()
    pg.quit()

# pg.draw.rect(surface, blue, (inicio[0] + i * block_size + padding_x,
#                                         inicio[1] + j * block_size + padding_y, 
#                                         block_size, 
#                                         block_size))

# elif event.type == pg.MOUSEBUTTONUP:
            #     for cuadrado in grid:
            #         if cuadrado.rect.collidepoint(mouse_pos):
            #             cuadrado.lightState = False

# if not(game.vs["titulo"]) and not(loose):
        #     game.draw(screen, "principal")   
        # elif game.vs["titulo"]:
        #     game.draw(screen, "inicio") 
        # else:
        #     screen.blit(fondo_rojo, (0,0))
        #     try:
        #        rojo.a -= 20
        #        fondo_rojo.fill(rojo)
        #     except:
        #         rojo.a = 0
        #     loose_screen(nivel, button_exit, button_retry)
        
# if not(titulo):
                #     for cuadrado in grid:
                #         if cuadrado.rect.collidepoint(mouse_pos) and not(jugando) and not(loose):
                #             cuadrado.light_state = True
                #         elif cuadrado.rect.collidepoint(mouse_pos) and jugando and cuadrado.choosen == True and not(loose):
                #             cuadrado.light_state = True
                #             cuadrado.choosen = False
                #         elif cuadrado.rect.collidepoint(mouse_pos) and jugando and cuadrado.choosen == False and not(loose):
                #             contador = time_now
                #             loose = True

# if button_exit.collidepoint(mouse_pos) and loose and time_now > contador + 0.5:
#     run = False
    
# if button_retry.collidepoint(mouse_pos) and loose and time_now > contador + 0.5:
#     run = False
#     grid.empty() #* muy importante ya que reinicia el grid
#     main()

# if game.vs["animacion"] and time_now > game.vs["contador"] + 1:
        #     game.vs["jugando"] = game.vs["anim"].animar()
        #     if game.vs["jugando"] != None:
        #         game.vs["jugando"] = True
        #         game.vs["animacion"] = False