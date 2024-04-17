states = {0: "ready to move, then attack",
          1: "ready to attack, already moved",
          2: "ready to attack ? can still move",
          3: "turn ended"}


class Character:
    Instances = []

    def __init__(self, name, hp, atk, res, spd, rng, sprites):
        if len(name) > 3:
            name = name[:3]
        self.name = name
        self.coord = None
        self.state = 0

        self.maxhp = hp
        self.hurt = 0
        self.power = atk
        self.resistance = res
        self.move = spd
        self.range = rng

        self.sprites = sprites

        Character.Instances.append(self)

    def Get_HP(self):
        ans = self.maxhp - self.hurt
        if ans > 0:
            return ans
        else:
            return False

    def Get_Move(self):
        ans = []
        for y in range(-self.move, self.move + 1):
            move_left = self.move - abs(y)
            for x in range(-move_left, move_left + 1):
                if (x, y) != (0, 0):
                    ans.append((x + self.coord[0], y + self.coord[1]))
        return ans

    def Possible_Move(self, dimension):
        maxx, maxy = dimension
        ans = []
        for coord in self.Get_Move():
            if 0 <= coord[0] < maxx and 0 <= coord[1] < maxy:
                ans.append(coord)
        return ans

    def Damage(self, damage, phys=True):
        if not self.Get_HP():
            print(self.name + " is already KO.")
            return False
        if phys:
            damage -= self.resistance
        if damage <= 0:
            print(self.name + " didn't get a scratch.")
            return 0
        self.hurt += damage
        print(self.name + " took " + str(damage) + " damage.")
        if not self.Get_HP():
            print(self.name + " is fucking dead.")
        else:
            print("They have " + str(self.Get_HP()) + " hp left.")
        return damage

    def Attack(self, target):
        print(self.name + " attacked " + target.name + ".")
        return target.Damage(self.power)

    def Get_Range(self, dimension):
        maxx, maxy = dimension
        ans = []
        for rng in self.range:
            for y in range(-rng, rng + 1):
                rng_left = rng - abs(y)
                for x in range(-rng_left, rng_left + 1):
                    if abs(x) + abs(y) == rng and (x, y) != (0, 0):
                        if 0 <= x + self.coord[0] < maxx and 0 <= y + self.coord[1] < maxy:
                            ans.append((x + self.coord[0], y + self.coord[1]))
        return ans

    def __repr__(self):
        return self.name
