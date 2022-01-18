import os
from test_to_dict_or_list import test_to_list
from random import shuffle
from glob import glob
from tkinter import simpledialog
import tkinter
''' ---- what is this?

	This takes a txt file with questions and answers:

	What is the capital of italy
	Rome
	Paris
	...

	and print to console the text to paste
	in the excel sheet template dowloaded from kahoot
	so that is accepted for creating a quiz importing it
		after you copied do the guided import putting
		the ; as separator

end ---- '''

def kahoot():
	# print(kh)
	shuffle(kh) # mischio le liste delle liste con d,r,r,r,r
	for n,d in enumerate(kh):
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
	html = ""
	for n,d in enumerate(kh):
		print(*d, sep = ";")
		html += ";".join(d)
	simpledialog.messagebox("title",html)

	# print("Numero domande: " + str(len(kh)))


# converte in lista di liste il testo qui sopra
folder = "dati"
def get_text():
	import os
	files = glob(f"{folder}/*.txt")
	for n,f in enumerate(files):
		print(n,f)
	num = int(input("Numero del file con le domande: "))
	filedaaprire = files[num]
	with open(filedaaprire, "r", encoding="utf-8") as file:
		file = file.read()
	return file

# Ricorda: per trasformare i file di testo per kahoot (togliendo #)
# usa trasformaFileDiTestoPerKahoot.py
kh = test_to_list(get_text())
kahoot()



