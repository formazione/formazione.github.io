# crea un compito dalle domande
import os

elenco = os.listdir()
[print(n,i) for n,i in enumerate(elenco)]
scelta = int(input("Num>"))
print(elenco[scelta])