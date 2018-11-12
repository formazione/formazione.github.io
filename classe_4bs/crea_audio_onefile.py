#crea_audio.py
import glob
from gtts import gTTS
import os

def saveaudio(text, name):
	tts = gTTS(text, lang='it')
	print(text)
	tts.save(name)
	os.system(name)

def inseriscinomefile():
	print(" ==== file di testo da convertire in audio ===")
	listafile = glob.glob("*.txt")
	for n,file in enumerate(listafile):
		print(n, file)
	print(" =============================================")
	print()
	num_file = int(input("Numero del file di testo da trasformare > "))
	return listafile[num_file][:-4]

text = inseriscinomefile()

n = 0
html = "<script src=\"audio.js\"></script><script> audiojs.events.ready(function() {var as = audiojs.createAll(); }); </script>"
with open(text + ".txt", 'r', encoding="utf-8") as file:
	testo = file.read()
	file.seek(0)
	for line in file.readlines():
		if line == "\n":
			pass
		elif line[-2] == "?":
			html += "<h2>" + line + "</h2>"
		else:
			html += "<div id='mp3'" + str(n) + ">" + line + "</p>"
name = input("Nome del file mp3? > ") + ".mp3"
html += "<audio preload=\"auto\"> <source src='" + name + "''> </audio>"
with open(text + ".html", "w", encoding='utf-8') as file:
	file.write(html)
os.system(text + ".html")
saveaudio(testo, name)

			#os.system(name)

