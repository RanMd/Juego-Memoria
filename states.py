import pygame as pg
from random import choice, choices
from piezas import Animation
from piezas import Cuadrito

def chose_squares(cuadrados: pg.sprite.Group, nivel: int):
    chosens = choices(cuadrados.sprites(), k= nivel)
    for chosen,i in zip(chosens, range(1, len(chosens) + 1)):
        chosen.orden.append(i)
    return chosens  

def add_square(cuadrados: pg.sprite.Group, lista_hecha:list, cantidad = 1):
    for x in range(cantidad):
        lista_hecha.append(choice(cuadrados.sprites()))
        
    for chosen,i in zip(lista_hecha, range(1, len(lista_hecha) + 1)):
        chosen.orden.append(i)
    return lista_hecha
      

white = pg.Color(255, 255, 255)
black = pg.Color(0, 0, 0)
mine_font = pg.font.match_font('Helvetica')
size = (400, 310)
block_size = 60

def show_text(pantalla, fuente, texto, color, tam, xy):
    tipo_letra = pg.font.Font(fuente, tam)
    text = tipo_letra.render(texto, True, color)
    rect_text = text.get_rect()
    rect_text.center = xy
    pantalla.blit(text, rect_text) 
    
grid = pg.sprite.Group()   

def name_grid(grid):
    for cuadrito,i in zip(grid, range(1,len(grid) + 1)):
        cuadrito.nombre = i
        
def create_grid(cantidad, block_size, inicio = (0,0)):
    padding_x = 0
    padding_y = 5
    for i in range(cantidad):
        for j in range(cantidad):
            if (i,j) == (0,0):
                cuadrado = Cuadrito(inicio[0] + i * block_size, inicio[1] + j * block_size, block_size, block_size)
                grid.add(cuadrado)
                continue
            
            cuadrado = Cuadrito(inicio[0] + i * block_size + padding_x, inicio[1] + j * block_size + padding_y, block_size, block_size)
            grid.add(cuadrado)
            padding_y += 5
            
        padding_x += 5
        padding_y = 0
    name_grid(grid)
    return grid


class Game():
    def __init__(self):
        self.vs = {
            "retry": False,
            "jugando": False,
            "run": True,
            "grid": create_grid(3, block_size, (105, 80)),
            "nivel": 1,
            "chosens": [],
            "anim": None,
            "animacion": False,
            "contador": 0,
            "state": "inicio"          
        }
        self.states = {
            "inicio": Inicio(),
            "principal": Principal(self.vs["grid"], self.vs["nivel"]),
            "loose": Loose(self.vs["nivel"])
        }
        
    def event_handler(self, estado:str, game, mouse_pos, time_now):     
        self.states[estado].collision(mouse_pos, game, time_now)
        
    def draw(self, surface: pg.Surface, estado:str):
        self.states[estado].draw(surface)
        
    def update(self, estado:str):
        self.states[estado].update()
        
    def animar(self, time_now:int):
        if self.vs["animacion"] and time_now > self.vs["contador"] + 750:
            self.vs["jugando"] = self.vs["anim"].animar()
            if self.vs["jugando"] != None:
                self.vs["jugando"] = True
                self.vs["animacion"] = False

class Inicio():
    def __init__(self):
        self.image = pg.image.load("images/inicio.png").convert()
        self.button_start = pg.Rect(145, 230, 100, 40)
        
    def draw(self, surface: pg.Surface):
        surface.blit(self.image, (25, 20))
        
    def collision(self, mouse_pos:tuple, game:Game, time_now:int):
        if self.button_start.collidepoint(mouse_pos):
            game.vs["chosens"] = add_square(game.vs["grid"], game.vs["chosens"])    #chose_squares(game.vs["grid"], game.vs["nivel"])
            game.vs["anim"] = Animation(game.vs["chosens"])
            game.vs["animacion"] = True
            game.vs["contador"] = time_now
            game.vs["state"] = "principal"
        
    def update(self):
        pass
        
        
class Principal():
    def __init__(self, grid:pg.sprite.Group, nivel):
        self.grid = grid
        self.nivel = nivel
        self.next_level = False
        self.white = pg.Color(white)
        self.fondo_blanco = pg.Surface(size, flags=pg.SRCALPHA)
        self.fondo_blanco.fill(self.white)
        self.orden = 1
        self.loose = False
        
    def draw(self, surface:pg.Surface):
        show_text(surface, mine_font, f"Nivel: {self.nivel}", white, 25, (200, 40))
        self.grid.draw(surface)
        if self.next_level:
            surface.blit(self.fondo_blanco, (0,0))
        
    def collision(self, mouse_pos:tuple, game:Game, time_now:int):
        for cuadrado in game.vs["grid"]:
            if cuadrado.rect.collidepoint(mouse_pos) and not(game.vs["jugando"]):
                cuadrado.light_state = True
            elif cuadrado.rect.collidepoint(mouse_pos):
                cuadrado.light_state = True
                self.next_level = self.level_up(game , cuadrado)
                
        if self.next_level:
            self.nivel += 1
            game.vs["animacion"] = True
            game.vs["contador"] = time_now
            game.vs["nivel"] += 1
            game.vs["chosens"] = add_square(game.vs["grid"], game.vs["chosens"])
            game.vs["anim"] = Animation(game.vs["chosens"])
            game.vs["jugando"] = False
            
        if self.loose:
            game.vs["state"] = "loose"
            game.states["loose"].set_level(self.nivel)
                
    def update(self):
        self.grid.update()
        self.pass_level()
        
    def level_up(self, game:Game, cuadrado:Cuadrito):
        if len(cuadrado.orden) == 0:
            self.loose = True
            return
            
        if self.orden != cuadrado.orden[0]:
            self.loose = True
        else:
            self.orden += 1
            cuadrado.orden.pop(0)
            if self.orden > len(game.vs["chosens"]):
                self.orden = 1
                return True
            
    
    def pass_level(self):
        if not self.next_level:
            return
        
        self.fondo_blanco.fill(self.white)
        try: #no deberia, pero funciona
            self.white.a -= 15
        except:
            self.next_level = False
            self.white.a = 255
            self.orden = 1
        
            
class Loose():
    def __init__(self, nivel):
        self.rojo = pg.Color(245, 151, 148, 255)
        self.fondo_rojo = pg.Surface(size, flags= pg.SRCALPHA)
        self.fondo_rojo.fill(self.rojo)
        self.button_exit = pg.Rect(90,180,100,40)
        self.button_retry = pg.Rect(210,180,100,40)
        self.nivel = nivel
        
    def draw(self, surface:pg.Surface):
        surface.blit(self.fondo_rojo, (0,0))
        show_text(surface, mine_font, f"Nivel {self.nivel}", white, 30, (200, 120))
        pg.draw.rect(surface, (255, 209, 84), self.button_exit, border_radius= 3)
        pg.draw.rect(surface, (149, 195, 232), self.button_retry, border_radius= 3)
        show_text(surface, mine_font, "Salir", black, 15, (140, 200))
        show_text(surface, mine_font, "Reiniciar", black, 15, (260, 200))
        
    def update(self):
        self.fondo_rojo.fill(self.rojo)
        try:
            self.rojo.a -= 20
        except:
            self.rojo.a = 0
            
    def collision(self, mouse_pos, game:Game, time_now:int):
        if self.button_exit.collidepoint(mouse_pos):
            game.vs["run"] = False
        
        if self.button_retry.collidepoint(mouse_pos):
            game.vs["run"] = False
            game.vs["grid"].empty() #* muy importante ya que reinicia el grid
            game.vs["retry"] = True
            
    def set_level(self, valor:int):
        self.nivel = valor