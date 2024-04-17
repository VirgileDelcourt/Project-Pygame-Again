import pygame


class Display(pygame.sprite.Sprite):
    Instances = []

    def __init__(self, animation, coord, master=None):
        super().__init__()
        self.master = master
        if self.master:
            animation = self.master.sprites
            if self.master.coord is not None:
                coord = self.master.coord

        self.animation = animation
        self.current_image = 0
        self.timer = 0

        self.active = True
        self.tinted = False
        self.coord = coord
        self.Load_Img()

        Display.Instances.append(self)

    def Load_Img(self, source=None):
        if source is None:
            source = self.animation[self.current_image][0]
        self.surf = pygame.image.load(source).convert_alpha()
        self.rect = self.surf.get_rect()
        self.Update_Rect()

    def Update_Rect(self, coord=None):
        if coord is None:
            x, y = self.coord
        else:
            self.coord = coord
            x, y = coord
        self.rect.topleft = x * 100, y * 100

    def Set_Active(self, active=True):
        self.active = active

    def Update(self, delta_time):
        if self.master is None:
            self.Update_Rect(self.master.coord)
            return

        if not self.master.Get_HP():
            self.Set_Active(False)
            return
        else:
            self.Set_Active(True)

        if self.master.state == 3 and not self.tinted:
            self.tinted = True
        elif self.master.state == 0 and self.tinted:
            self.tinted = False

        self.timer += delta_time
        if self.timer >= self.animation[self.current_image][1]:
            self.timer -= self.animation[self.current_image][1]
            self.current_image += 1
            if self.current_image >= len(self.animation):
                self.current_image = 0

        self.Load_Img()
        if self.tinted:
            self.surf.fill((100, 100, 100, 0), special_flags=pygame.BLEND_MULT)
        self.Update_Rect(self.master.coord)
