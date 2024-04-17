import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, coords):
        super().__init__()
        self.x, self.y = coords
        self.surf = pygame.Surface((100, 100))
        self.rect = self.surf.get_rect()
        self.surf.fill("white")
        self.rect.topleft = self.x * 100, self.y * 100

    def Color(self, color):
        self.surf.fill(color)
