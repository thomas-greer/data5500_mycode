from Rectangle import *
from Employee import *
from Pet import *

#Easy Question
r1 = Rectangle(3,7)
r1.findArea()
r2 = Rectangle(14,204)
r2.findArea()

#Medium Question
e1 = Employee("John", 5000)
e1.salaryIncrease(.1)

#Hard Question
p1 = Pet("Jane", 3, "Cat")
p2 = Pet("Wilford", 8, "DOG")
p3 = Pet("Milly", 26, "elephant")
p4 = Pet("Michael", 8, "Lizard")

p1.calcAge()
p2.calcAge()
p3.calcAge()
p4.calcAge()
