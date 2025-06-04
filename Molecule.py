class Molecule:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def posisjon(self):
        return (self.x,self.y,self.z)