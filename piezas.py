import pygame as pg

class Cuadrito(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, nombre = 1):
        super().__init__()
        self.blue = pg.Color(36, 114, 192)
        self.white = pg.Color(255, 255, 255)
        self.color_anim = pg.Color(36, 114, 192)
        self.image = pg.Surface((width, height), pg.SRCALPHA)
        self.image.fill((self.blue))
        self.rect = self.image.get_rect(topleft = (x,y)) # con el parametro topleft agrego las coordenadas x y de una vez
        self.orden = []
        self.animation = False
        self.light_state = False
        self.nombre = nombre
        
    def update(self):
        self.image.fill(self.color_anim)
        self.illuminate()
                
    def illuminate(self):
        if not(self.light_state):
            self.color_anim.update(self.change_color(self.color_anim, self.blue, 15))
        else:
            self.animation = True
            self.color_anim.update(self.change_color(self.color_anim, self.white, 15))
            if self.white == self.color_anim:
                self.light_state = False
        
        if self.blue == self.color_anim:
            self.animation = False
    
    def __repr__(self):
        return f"Cuadrito: {self.nombre} y debo ser: {self.orden}"
    
    @staticmethod
    def change_color(color_a, color_b, paso) -> tuple:
        if color_a == color_b:
            return color_a
        
        r = Cuadrito.change_component(color_a.r, color_b.r, paso)
        g = Cuadrito.change_component(color_a.g, color_b.g, paso)
        b = Cuadrito.change_component(color_a.b, color_b.b, paso)
        
        return (r, g, b)
            
    @staticmethod
    def change_component(component_a, component_b, paso):
        if component_a == component_b:
            return component_a
        
        if component_a < component_b:
            component_a += paso
            if component_a > component_b:
                component_a = component_b
        else:
            component_a -= paso
            if component_a < component_b:
                component_a = component_b
        
        return component_a
    
class Animation():
    def __init__(self, *args):
        self.start = False
        self.orden = 0
        self.objs = []
        for obj in args[0]:
            self.objs.append(obj)
        self.objs = tuple(self.objs)
            
    def animar(self):
        if self.orden == len(self.objs):
            self.start = False
            return self.start
        
        self.cambiar(self.objs[self.orden])
    
    def cambiar(self, sprite):
        if not(sprite.animation) and not(self.start):
            sprite.light_state = True
            self.start = True
            
        elif not(sprite.animation) and self.start:
            self.start = False
            self.orden += 1

    def __repr__(self) -> str:
        conjunto = []
        for cuadrito in self.objs:
            conjunto.append(cuadrito)
            
        return str(conjunto)

        
    # self.vanishState = False
    # def vanish(self, mouse_pos):
    #     if self.rect.collidepoint(mouse_pos):
    #         for i in range(255):
    #             self.blue.r = i
    #             self.update()
    
    # def vanish(self):
    #     """Desaparece el cuadrado"""
        
    #     if not(self.vanishState):
    #         return
    #     else:
    #         if self.alpha > 0:
    #             self.blue.a = self.alpha
    #             self.alpha -= 20
    #         else:
    #             self.kill()