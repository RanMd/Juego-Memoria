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
