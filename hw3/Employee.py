class Employee:
    def __init__(self, name, salary):
        self.name = name
        self. salary = salary

    def salaryIncrease(self, amount):
        print("Current Salary:", self.salary)
        amount += 1
        self.salary = amount * self.salary
        print("Updated Salary:", self.salary)

    