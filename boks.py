
class RektangelBoks:
    def __init__(self, bredde, høyde, dybde):
        self.bredde = bredde
        self.høyde = høyde
        self.dybde = dybde

    def volum(self):
        return self.bredde * self.høyde * self.dybde

    def overflate(self):
        b = self.bredde
        h = self.høyde
        d = self.dybde
        return 2 * (b*h + b*d + h*d)

    def beskriv(self):
        print(f"Boks med bredde {self.bredde}, høyde {self.høyde}, dybde {self.dybde}")
        print(f"Volum: {self.volum()} | Overflate: {self.overflate()}")
