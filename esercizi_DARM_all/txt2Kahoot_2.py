import os
from test_to_dict_or_list import test_to_list
from random import shuffle

def kahoot():
	print(kh)
	shuffle(kh) # mischio le liste delle liste con d,r,r,r,r
	for n,d in enumerate(kh):
		# d = [d,r,r,r,r]
		# n = numero della lista delle domande => [d,r,r,r]
		# memorizza la domanda
		# togli la domanda dalla lista
		# mischia le risposte restanti
		# rimetti la domanda all'inizio
		# crea la riga per excel con ;
		domanda = d[0] # memorizzo domanda d[0]
		giusta = d[1] # memorizza risposta giusta
		d.pop(0) # tolgo la domanda dalla lista d
		shuffle(d) # mischio le risposte rimaste
		index_giusta = d.index(giusta) + 1 # posizione della giusta
		if len(d) == 2:
			d.append("")
		if len(d) == 3:
			d.append("")
		d.insert(0,domanda) # se ricordo bene, si fa così?
		d.append(20) # aggiungo la durata in secondi
		d.append(index_giusta) # aggiungo la risposta giusta
	# stampiamo per kahoot
	for n,d in enumerate(kh):
		print(*d, sep = ";")
	print("Numero domande: " + str(len(kh)))


# converte in lista di liste il testo qui sopra
dir = "dati"
def get_text():
	import os
	files = os.listdir(dir)
	for n,f in enumerate(files):
		print(n,f)
	num = int(input("Numero del file con le domande: "))
	filedaaprire = os.listdir(dir)[num]
	with open(dir + "/" + filedaaprire, "r", encoding="utf-8") as file:
		file = file.read()
	return file

# Ricorda: per trasformare i file di testo per kahoot (togliendo #)
# usa trasformaFileDiTestoPerKahoot.py
kh = test_to_list(get_text())
kahoot()



