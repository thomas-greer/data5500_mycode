class Food:
    def __init__(self, name, flavor, color, rating, texture):
        self.name = name
        self.flavor = flavor
        self.color = color
        self.rating = rating
        self.texture = texture

    def __str__(self):
        return f"{self.name} (flavor: {self.flavor}, color: {self.color}, rating: {self.rating}, texture: {self.texture})"

    def recommend(self):
        if self.rating >= 7:
            print(self.name, "is a recommended food.")
        else:
            print(self.name, "is not a recommended food.")
    
    def setFlavor(self, newFlavor):
        self.flavor = newFlavor
    
    def setRating(self, newRating):
        self.rating = newRating

    def throwability(self):
        if self.texture.lower() in ("gritty", "thick"):
            print("You throw the food.")


    
pizza = Food("pizza", "savory", "orange", 8, "thick")

pizza.throwability()
print(pizza)