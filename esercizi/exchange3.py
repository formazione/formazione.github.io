import random

class Exchange:
    '''e1 = Exchange(dollars=1000, euro=1, exchange_rate=1.18) will give you the euro for 1000 $\
    d1 = Exchange(dollars=1, euro=500, exchange_rate=1.18)
    '''
    def __init__(self, dollars, euro, exchange_rate):
        "If euro = 1 it changes dollars into euro and viceversa"
        self.dollars = dollars
        self.euro = euro
        self.exchange_rate = exchange_rate

    def exchange(self):
        "Calculate euro for dollars and viceversa"
        if self.euro: # get euro for .... dollars
            return round(self.dollars / self.exchange_rate, 2)
        if self.dollars:
            return round(self.euro * self.exchange_rate, 2)

    def print(self):
        "This just adds the € to the euro"
        print(f"{self.euro} €")
    
    def pprint(self, lang="en"):
        if lang == "en":
            self.print_sol = f"You get {self.dollars} $ for [{self.exchange()} €] "
            self.print_sol += f" at an exchange rate of {self.exchange_rate}"
        else:
            self.print_sol = f"Ottieni {self.dollars} $ per [{self.exchange()} €] "
            self.print_sol += f" cal exchange_rate di {self.exchange_rate}"
        #print(self.print_sol)
        return self.print_sol

    def print_ex(self, lang="en"):
        "Call this to print the exercises"
        global cnt

        if self.euro:
            d = self.dollars
            c = self.exchange_rate
            if lang=="en":
                f = [
                    f"How many € you must give to get {d} $ at and exchange rate of {c}?",
                    f"Change {d} $ in euro at an exchange rate of {c}.",
                    f"How many € you must pay to get {d} $ at and exchange rate of {c}?",
                    f"Find the € you need to buy {d} $ at and exchange rate of {c}.",
                    f"If you got {d} $, how many euro you will get at {c} as exchange rate?"
                ]
            if lang=="it":
                f = [
                    f"Quanti € devi pagare per acquistare {d} $ al exchange_rate EUR/USD di {c}?",
                    f"Cambia {d} $ in euro al tasso di {c}.",
                    f"Calcola quanti euro ottieni vendendo {d} $ al exchange_rate pari a {c} EUR/USD.",
                    f"Con {d}$, quanti euro ottieni con un exchange_rate EUR/USD pari a {c}?"
                ]

        self.print_change = f"{cnt}. {random.choice(f)}"
        print(self.print_change)
        cnt += 1
        return self.print_change

    def dollars(self):
        if self.euro != 1:
            return self.euro() * self.exchange_rate

    def random(self):
        return random.randrange(100, 3000, 50)

    def random_exchange_rate(self):
        ch = 1 + round(random.random(), 2)
        # print(ch)
        return ch

    def generate_ex(self):
        "generates random dollars and exchange"
        self.exchange_rate = round(self.random_exchange_rate(), 2)
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
def main(save=0, solutions=0, number=10, html=1, lang="it"):
    "This shows 10 random exercizes made with the class Exchange"
    ################## Instructions ####################
    # first create an istance

    e1 = Exchange(dollars=1000, euro=1, exchange_rate=1.18)
    # See how many euro you can get from 1000 $ with e1.pprint()
    # e1.pprint()

    # Let's create 10 exercizes
    sol = []
    text = []
    # change 10 if you want more or less exercizes
    print("Solve these exercizes:\n ---")
    for n in range(number):
        # Generate a random exercise
        e1.generate_ex()
        # adds the exercise to the list sol
        sol.append(str(cnt) + ". " + e1.pprint(lang))
        e1.print_ex(lang)
        text.append(e1.print_change)
        # prints traccia and solutions
    print_solutions(sol)
    if save:
        if solutions:
            save_solutions(sol)
            save_text_n_sol(text, sol, html)
            save_text(text)
        else:
            save_text(text)


def save_text(text):
    "Create text file"
    text = [t for n,t in enumerate(text)]
    text = "\n".join(text)

    with open("traccia.txt", "w") as file:
        file.write(text)

def save_solutions(sol):
    "Create text file"
    sol = [t for t in sol]
    sol = "\n".join(sol)

    with open("soluzione.txt", "w") as file:
        file.write(sol)


def save_text_n_sol(text, sol, html):
    "Create text file"
    if html == 0:
        # text = [str(n + 1) + " " + t for n,t in enumerate(text)]
        text = "\n".join(text)
        sol = [str(n + 1) + " " + t for n,t in enumerate(sol)]
        sol = "\n".join(sol)

        with open("text_n_sol.txt", "w") as file:
            file.write("Exercises:\n")
            file.write(text)
            file.write("\n\nSolutions:\n")
            file.write(sol)
    else:
        text = [f"<p>{t}</p>" for n,t in enumerate(text)]
        text = "\n".join(text)
        sol = [f"<p>{t}</p>" for n,t in enumerate(sol)]
        sol = "\n".join(sol)
        with open("text_n_sol.html", "w") as file:
            file.write("<h2>Exercises:</h2>")
            file.write(text)
            file.write("<h2>Solutions:</h2>")
            file.write(sol)


def print_solutions(sol):
    "Prints the solutions"
    print("\nSolutions")
    # print only solutions
    for n in sol:
        print(n)

main(
    save=1, # to save a text file for the students
    solutions=1, # the text with solutions for the teacher
    number=5, # how many exercises about exchange rate
    html=1, # you get an html file for the students
    lang="en") # you can choose en or it as language
