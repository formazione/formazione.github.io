import random

class Exchange:
    '''e1 = Exchange(dollars=1000, euro=1, cambio=1.18) will give you the euro for 1000 $\
    d1 = Exchange(dollars=1, euro=500, cambio=1.18)
    '''
    def __init__(self, dollars, euro, cambio):
        "If euro = 1 it changes dollars into euro and viceversa"
        self.dollars = dollars
        self.euro = euro
        self.cambio = cambio

    def exchange(self):
        "Calculate euro for dollars and viceversa"
        if self.euro:
            return round(self.dollars / self.cambio, 2)
        if self.dollars:
            return round(self.euro * self.cambio)

    def print(self):
        "This just adds the € to the euro"
        print(str(self.euro + " €")
    
    def pprint(self):
        self.print_sol = f"You get {self.dollars} $ for [{self.exchange()} €] "
        self.print_sol += f" at an exchange rate of {self.cambio}"
        print(self.print_sol)
        return self.print_sol

    def print_ex(self):
        if self.euro:
            d = self.dollars
            c = self.cambio
            f = [
                f"How many € you must give to get {d} $ at and exchange rate of {c}?",
                f"Change {d} $ in euro at an exchange rate of {c}.",
                f"How many € you must pay to get {d} $ at and exchange rate of {c}?",
                f"Find the € you need to buy {d} $ at and exchange rate of {c}.",
                f"If you got {d}$, how many euro you will get at {c} as exchange rate?"
                ]

        self.print_change = random.choice(f)
        print(self.print_change)
        return self.print_change

    def dollars(self):
        if self.euro != 1:
            return self.euro() * self.cambio

    def random(self):
        return random.randrange(100, 3000, 50)

    def random_cambio(self):
        ch = 1 + round(random.random(), 2)
        # print(ch)
        return ch

    def generate_ex(self):
        "generates random dollars and exchange"
        self.cambio = round(self.random_cambio(), 2)
        if self.euro == 1:
            self.dollars = self.random()
            self.result = self.exchange()
        else:
            self.euro = self.random()
            self.result = self.exchange()

    def print_solution(self):
        print("Solution:")
        self.pprint()
        print()

# if you want to make exercize just give and example of data
e1 = Exchange(dollars=1000, euro=1, cambio=1.18)
# e1.pprint()
sol = []
for n in range(10):
    e1.generate_ex()
    sol.append(e1.pprint())
    e1.print_ex()

print("\nSolutions")

for n in sol:
    print(n)
