from Tile import Tile


class Field:
    def __init__(self, dim):
        _x, _y = dim
        self.map = []
        for y in range(_y):
            self.map.append([])
            for x in range(_x):
                self.map[-1].append(Tile((x, y)))

    def Get(self, coord):
        x, y = coord
        return self.map[y][x]
    
    def Get_Dim(self):
        return len(self.map[0]), len(self.map)

    def Get_All(self):
        ans = []
        for row in self.map:
            ans.extend(row)
        return ans

    def Color(self, color, coords):
        a, o = self.Get_Dim()
        for coord in coords:
            if 0 <= coord[0] <= a and 0 <= coord[1] <= o:
                self.Get(coord).Color(color)

    def Blit_All(self, window):
        for tile in self.Get_All():
            window.blit(tile.surf, tile.rect)
            
    def funny_colors(self):
        a, o = self.Get_Dim()
        for y in range(o):
            for x in range(a):
                if (x + y) % 2 == 0:
                    self.Get((x, y)).Color("green")
                else:
                    self.Get((x, y)).Color("dark green")
