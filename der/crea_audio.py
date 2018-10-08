#crea_audio.py
import glob
from gtts import gTTS
import os

text = "prova.txt"
n = 1
html = "<script src=\"audio.js\"></script><script> audiojs.events.ready(function() {var as = audiojs.createAll(); }); </script>"
with open(text, 'r', encoding="utf-8") as file:
	for line in file.readlines():
		if line == "\n":
			pass
		elif line[-2] == "?":
			print(line)
			name = text[:-4] + str(n) + ".mp3"
			html += "<h2><a href='" + name + "' onclick=javascript:mp3" + str(n) +".innerHTML='ciao'>" + line + "</a></h2>"
			# html += "<audio id='speak'><source src='" + name + "' type='audio/mpeg' /></audio>"
			html += "<audio preload=\"auto\"> <source src='" + name + "''> </audio>"
			n += 1
			pass
		else:
			html += "<div id='mp3'" + str(n) + ">" + line + "</p>"
			name = text[:-4] + str(n) + ".mp3"
			html += "<audio preload=\"auto\"> <source src='" + name + "''> </audio>"
			n += 1
			x = 0
			if x == 1:
				tts = gTTS(line, lang='it')
				name = text[:-4] + str(n) + ".mp3"
				print(name)
				tts.save(name)
			#os.system(name)

with open("prova.html", "w", encoding='utf-8') as file:
	file.write(html)
os.system("prova.html")