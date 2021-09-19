a = {
"Breglia" : {},
"Brunone" : {},
"Cammarano D" : {},
"Cammarano N" : {},
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
"Scola M" : {},
"Scola V" : {},
}

def alunno(nome, punti):
       a[nome][dd] = punti


def day(dd):
       for k in a:
              a[k][dd] = 0
       return dd
# ===================== 20.9
dd = day("18.9")
alunno("Malzone", 3)
alunno("Mandia", 7)
alunno("Musto", 1)

# ======================== 20.9 
dd = day("20.9")
# a["Mandia"][dd] = 5
# a["Mandia"][dd] = 10
alunno("Mandia", 2)


# ====================== 22 settembre
dd = day("22.9")
alunno("Mandia", 0)


# ================ end update score ========