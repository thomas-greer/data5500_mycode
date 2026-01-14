class Pet:
    def __init__(self, name, age, species):
        self.name = name
        self.age = age
        self.species = species
    
    def calcAge(self):
        if self.species.lower() == "dog":
            print("Name:", self.name, "\nAge:", str(self.age * 7))
        elif self.species.lower() == "cat":
            print("Name:", self.name, "\nAge:", str(self.age * 3))
        elif self.species.lower() == "elephant":
            print("Name:", self.name, "\nAge:", str(self.age * .5))
        else:
            print("We dont know the calculation for that Animal")