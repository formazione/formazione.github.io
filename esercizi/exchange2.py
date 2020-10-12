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
        if self.euro: # get euro for .... dollars
            return round(self.dollars / self.cambio, 2)
        if self.dollars:
            return round(self.euro * self.cambio, 2)

    def print(self):
        "This just adds the € to the euro"
        print(f"{self.euro} €")
    
    def pprint(self):
        self.print_sol = f"You get {self.dollars} $ for [{self.exchange()} €] "
        self.print_sol += f" at an exchange rate of {self.cambio}"
        #print(self.print_sol)
        return self.print_sol

    def print_ex(self, lang="en"):
        "Call this to print the exercises"
        global cnt

        if self.euro:
            d = self.dollars
            c = self.cambio
            if lang=="en":
                f = [
                    f"How many € you must give to get {d} $ at and exchange rate of {c}?",
                    f"Change {d} $ in euro at an exchange rate of {c}.",
                    f"How many € you must pay to get {d} $ at and exchange rate of {c}?",
                    f"Find the € you need to buy {d} $ at and exchange rate of {c}.",
                    f"If you got {d}$, how many euro you will get at {c} as exchange rate?"
                ]
            if lang=="it":
                f = [
                    f"Quanti € devi pagare per acquistare {d} $ al cambio EUR/USD di {c}?",
                    f"Cambia {d} $ in euro al tasso di {c}.",
                    f"Calcola quanti euro ottieni vendendo {d} $ al cambio pari a {c} EUR/USD.",
                    f"Con {d}$, quanti euro ottieni con un cambio EUR/USD pari a {c}?"
                ]

        self.print_change = random.choice(f)
        print(str(cnt), self.print_change)
        cnt += 1
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
        # return self.euro, self.dollars, self.result

    def print_solution(self):
        print("Solution:")
        self.pprint()
        print()

cnt = 1
def main(save=0):
    "This shows 10 random exercizes made with the class Exchange"
    ################## Instructions ####################
    # first create an istance

    e1 = Exchange(dollars=1000, euro=1, cambio=1.18)
    # To see the result of the istance, uncomment the following statement
    # e1.pprint()

    # Let's create 10 exercizes
    sol = []
    text = []
    # change 10 if you want more or less exercizes
    print("Solve these exercizes:\n ---")
    for n in range(10):
        # Generate a random exercise
        e1.generate_ex()
        # adds the exercise to the list sol
        sol.append(str(cnt) + " " + e1.pprint())
        text.append(e1.print_change)
        # prints traccia and solutions
        e1.print_ex()
    solutions(sol)
    if save:
        save_text(text)


def save_text(text):
    "Create text file"

    with open("traccia.txt", "w") as file:
        file.write(text)


def solutions(sol):
    "Prints the solutions"
    print("\nSolutions")
    # print only solutions
    for n in sol:
        print(n)

main(save=1)
