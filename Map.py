class Map:
    def __init__(self, dimension):
        self.map = []
        for y in range(dimension[1]):
            self.map.append([])
            for x in range(dimension[0]):
                self.map[-1].append(None)

    def Get_Dim(self):
        """
        :return: a tuple containing, in order, the length and width of the map, as int
        """
        return len(self.map[0]), len(self.map)

    def Get(self, coord):
        """
        :param coord: a tuple of 2 ints, representing the coordinates of the tile from whom you'd like to know about
        :return: what that tile contains (normally, a Character or None)
        """
        x, y = coord
        return self.map[y][x]

    def Insert(self, char, coord):
        """
        Inserts char at coord. Does not work if the designated tile is already occupied.
        :param char: what you want to put at those coordinates
        :param coord: a set of coordinates (a tuple of 2 int)
        :return: the char you gave it if the insertion was successful, an error otherwise
        """
        if not self.Get(coord):
            x, y = coord
            self.map[y][x] = char
            char.coord = (x, y)
            return char
        else:
            raise RuntimeError("Tried to insert " + str(char) + " at " + str(coord) + " but tile was already occupied")

    def Pop(self, coord):
        """
        Remove content from the tile of coordinates coord.
        :param coord: a tuple of 2 int
        :return: the content of that tile if the removal was successful, False otherwise.
        """
        rep = self.Get(coord)
        if rep:
            x, y = coord
            self.map[y][x] = None
            return rep
        else:
            return False

    def In(self, char):
        for y in range(self.Get_Dim()[1]):
            for x in range(self.Get_Dim()[0]):
                rep = self.Get((x, y))
                if rep == char:
                    return (x, y)
        return False

    def Remove(self, char):
        """
        Instead of Pop, takes in a value and will remove the first occurence it founds
        :param char: what you want to delete from the map
        :return: char if the removal was successful, False otherwise
        """
        for y in range(self.Get_Dim()[1]):
            for x in range(self.Get_Dim()[0]):
                rep = self.Get((x, y))
                if rep == char:
                    return self.Pop(self.In(char))
        return False

    def Show(self, highlight="", coords=()):
        ans = "  "
        for i in range(self.Get_Dim()[0]):
            ans += " " + str(i) + "  "
        ans += "\n"
        for y in range(self.Get_Dim()[1]):
            ans += str(y) + " "
            for x in range(self.Get_Dim()[0]):
                if (x, y) in coords and self.Get((x, y)) is None:
                    ans += highlight + " "
                else:
                    ans += str(self.Get((x, y)))[:3] + " "
            ans += "\n"
        return ans[:-2]
    
    def __repr__(self):
        return "Map of size : " + str(self.Get_Dim())
