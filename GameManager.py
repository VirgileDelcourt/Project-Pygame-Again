class GameManager:
    Instance = None
    
    def __init__(self, _map, field):
        self.map = _map
        self.field = field
        self.selected = None
        
        GameManager.Instance = self
        
    def Select(self, coord):
        x, y = coord
        a, o = self.map.Get_Dim()
        if not (0 <= x <= a and 0 <= y <= o):
            raise RuntimeError("GameManager.Select received wrong coord : " + str(coord))
            
        if self.selected is None:
            get = self.map.Get((x, y))
            if get is not None and get.state != 3:
                self.selected = x, y
                self.Color_Act(get)
            return
        
        current = self.map.Get(self.selected)
        new = self.map.Get((x, y))
        
        if current.state == 0 and (x, y) in current.Possible_Move((a, o)) and new is None:
            self.map.Remove(current)  # movement
            self.map.Insert(current, (x, y))
            self.selected = x, y
            current.state = 1
            
        elif current.state == 0 and current == new:  # skip movement
            current.state = 2
            
        elif current.state == 0 and (x, y) not in current.Possible_Move((a, o)):
            if new is None:  # unselect
                current.state = 3
                self.selected = None
            else:  # select smth else
                current.state = 3
                self.selected = x, y

        elif current.state in (1, 2) and (x, y) in current.Get_Range(self.map.Get_Dim()):
            if new is not None:
                current.Attack(new)  # attack
                current.state = 3
                self.selected = None
            
        elif current.state in (1, 2) and (x, y) not in current.Get_Range(self.map.Get_Dim()):
            if new is None or new == current:  # unselect
                self.selected = None
            else:  # select smth else
                self.selected = x, y
            if current.state == 2:
                current.state = 0
            else:
                current.state = 3
                
        if self.selected is not None:
            self.Color_Act(self.map.Get(self.selected))
        else:
            self.field.funny_colors()
                
    def Color_Move(self, char):
        self.field.funny_colors()
        self.field.Color("blue", char.Possible_Move(self.map.Get_Dim()))
        
    def Color_Atk(self, char):
        self.field.funny_colors()
        self.field.Color("red", char.Get_Range(self.map.Get_Dim()))
        
    def Color_Act(self, char):
        if char.state == 0:
            self.Color_Move(char)
        elif char.state in (1, 2):
            self.Color_Atk(char)
                
        
