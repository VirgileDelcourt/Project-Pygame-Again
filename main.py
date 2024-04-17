import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN
from time import time

from Map import Map
from Character import Character
from GameManager import GameManager
from FieldManager import Field
from Display import Display


def Move(_map, char, coord):
    if char.coord is None:
        raise TypeError(char.name + " coords were None")
    if coord in char.Possible_Move(_map.Get_Dim()):
        _map.Remove(char)
        _map.Insert(char, coord)
        print(char.name + " moved to " + str(coord) + ".")
        return True
    else:
        return False


def Attack(char, target):
    if target.coord in char.Get_Range():
        char.Attack(target)


def Turn(_map, char, field):
    field.funny_colors()
    field.Color("blue", char.Possible_Move(_map.Get_Dim()))
    Update_All(field)

    print(end="\n\n\n\n\n\n")
    print("it is " + char.name + "'s turn")
    print()
    print(_map.Show("---", char.Possible_Move(_map.Get_Dim())))
    print()
    ans = input("Where do you want them to move ?\n(input the coordinates, like \'0, 0\')\n>> ")
    Move(_map, char, To_Coord(ans))

    field.funny_colors()
    field.Color("red", char.Get_Range())
    Update_All(field)

    print()
    print(_map.Show("-x-", char.Get_Range()))
    print()
    ans = input("Who do you want to attack ?\n(input the coordinates, like \'0, 0\')\n>> ")
    if To_Coord(ans) != (0, 0):
        Attack(char, _map.Get(To_Coord(ans)))

    field.funny_colors()
    Update_All(field)

    Check_HP(_map)
    print()
    print(_map.Show())


def To_Coord(text):
    if len(text) == 3:
        x, y = int(text[0]), int(text[2])
    elif len(text) == 4:
        x, y = int(text[0]), int(text[3])
    elif len(text) == 5:
        x, y = int(text[1]), int(text[3])
    else:
        raise RuntimeError("coords were not like '0, 0'")
    return x, y


def Check_HP(_map):
    for char in Character.Instances:
        if _map.In(char) and not char.Get_HP():
            _map.Remove(char)


def Update_All():
    window.fill("#f42069")
    for tile in field.Get_All():
        window.blit(tile.surf, tile.rect)
    for display in Display.Instances:
        if display.active:
            display.Update(delta_time)
            window.blit(display.surf, display.rect)

    if GameManager.Instance.selected is not None:
        char = game.Get(GameManager.Instance.selected)
        window.blit(font.render(char.name, 1, "white"), (dimx * 100 + 20, 20))
        window.blit(font.render("hp : " + str(char.Get_HP()), 1, "white"), (dimx * 100 + 20, 60))
        window.blit(font.render("move : " + str(char.move), 1, "white"), (dimx * 100 + 20, 100))
        mv = ""
        for rng in char.range:
            mv += str(rng) + " - "
        mv = mv[:-3]
        window.blit(font.render("range : " + mv, 1, "white"), (dimx * 100 + 20, 140))
    else:
        window.blit(font.render("select a", 1, "white"), (dimx * 100 + 20, 20))
        window.blit(font.render("character", 1, "white"), (dimx * 100 + 20, 50))
        window.blit(font.render("end turn", 1, "white"), (dimx * 100 + 20, (dimy - 1) * 100 + 30))
    pygame.display.update()


pygame.init()

dimx, dimy = 8, 5
game = Map((dimx, dimy))
window = pygame.display.set_mode((dimx * 100 + 200, dimy * 100))
field = Field((dimx, dimy))
GameManager(game, field)
font = pygame.font.Font(None, 50)

Character.Instances = []
pap = Character("Papapapa", 10, 2, 0, 2, [1], (("Images/pap.png", 0.5), ("Images/pap2.png", 0.5)))
pip = Character("Pip ip ip turi ip ip", 10, 1, 1, 2, [1, 2], (("Images/pip.png", 0.5), ("Images/pip2.png", 0.5)))
brd = Character("Brd, and by brd I mean bird !", 1, 1, 0, 1, [1], (("Images/bird.png", 0.5), ("Images/bird2.png", 0.5)))
tip = Character("Tip (torinippu)", 20, 1, 0, 2, [1], (("Images/tip.png", 0.5), ("Images/tip2.png", 0.5)))
til = Character("Til u twirl !", 10, 1, 0, 3, [1], (("Images/til.png", 0.5), ("Images/til2.png", 0.5)))
fet = Character("Fet's Luck (u red that wrong)", 10, 1, 0, 2, [1], (("Images/fet.png", 0.5), ("Images/fet2.png", 0.5)))
bil = Character("Bill Cypher", 999, 2, 1, 999, [5], (("Images/bil.png", 999), ))


game.Insert(pap, (1, 1))
game.Insert(pip, (0, 0))
game.Insert(fet, (0, 1))
game.Insert(bil, (4, 4))
game.Insert(brd, (4, 2))
game.Insert(tip, (7, 3))
game.Insert(til, (6, 4))

Display.Instances = []
for char in Character.Instances:
    Display("", (0, 0), char)

field.funny_colors()

loop = True
last = time()
try:
    while loop:
        delta_time = time() - last
        last = time()
        for event in pygame.event.get():
            if event.type == QUIT:
                loop = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos[0] // 100, event.pos[1] // 100
                    if 0 <= x < dimx and 0 <= y < dimy:
                        GameManager.Instance.Select((x, y))
                    elif x >= dimx and y == dimy - 1 and GameManager.Instance.selected is None:
                        for char in Character.Instances:
                            if char.Get_HP():
                                char.state = 0

        Check_HP(game)
        Update_All()

except:
    pygame.quit()
    raise
else:
    pygame.quit()
