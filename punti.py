import pickle
if __name__ == "__main__":
       from classe5ae import *

a = {
"Breglia" : {},
"Brunone" : {},
"Cammarano_D" : {},
"Cammarano_N" : {},
"Costantini" : {},
"Del Verme" : {},
"Esposito" : {},
"Fontana" : {},
"Garofalo" : {},
"Giordano" : {},
"Grimaldi" : {},
"Lista" : {},
"Malzone" : {},
"Mandia" : {},
"Marchesani" : {},
"Musto" : {},
"Ruocco" : {},
"Santoro" : {},
"Scola_M" : {},
"Scola_V" : {},
}

def alunno(nome, punti):
       a[nome][dd] = punti


def day(dd):
       for k in a:
              a[k][dd] = 0
       return dd

def save_first_time():
       global dd
       # ===================== 18.9
       dd = day("18.9")
       alunno("Malzone", 3)
       alunno("Mandia", 7)
       alunno("Musto", 1)

       # ======================== 20.9 
       dd = day("20.9")
       alunno("Breglia",     0)
       alunno("Brunone",     0)
       alunno("Cammarano_D", 1)
       alunno("Cammarano_N", 1)
       alunno("Costantini",  1)
       alunno("Del Verme",   0)
       alunno("Esposito",    0)
       alunno("Fontana",     0)
       alunno("Garofalo",    1)
       alunno("Giordano",    1)
       alunno("Grimaldi",    0)
       alunno("Lista",       0)
       alunno("Malzone",     1)
       alunno("Mandia",     16)
       alunno("Marchesani",  0)
       alunno("Musto",       7)
       alunno("Ruocco",      0)
       alunno("Santoro",     0)
       alunno("Scola_M",     0)
       alunno("Scola_V",     0)


       # ====================== 22 settembre
       dd = day("22.9")
       alunno("Breglia",     0)
       alunno("Brunone",     0)
       alunno("Cammarano_D", 0)
       alunno("Cammarano_N", 0)
       alunno("Costantini",  0)
       alunno("Del Verme",   0)
       alunno("Esposito",    0)
       alunno("Fontana",     0)
       alunno("Garofalo",    0)
       alunno("Giordano",    0)
       alunno("Grimaldi",    0)
       alunno("Lista",       0)
       alunno("Malzone",     0)
       alunno("Mandia",      0)
       alunno("Marchesani",  0)
       alunno("Musto",       0)
       alunno("Ruocco",      0)
       alunno("Santoro",     0)
       alunno("Scola_M",     0)
       alunno("Scola_V",     0)

       # ================ end update score ========
       print(a)

def save_pickle():
       import pickle
       file = open("punti.pkl", "wb")
       pickle.dump(a, file)
       file.close()

# save_first_time()

file = open("punti.pkl", "rb")
a = pickle.load(file)
file.close()
print(a)