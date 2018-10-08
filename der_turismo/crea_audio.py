# crea_audio.py
import glob
from gtts import gTTS
import os


def saveaudio(line, name):
    tts = gTTS(line, lang='it')
    name = filename[:-4] + str(n) + ".mp3"
    print(name)
    tts.save(name)


def inseriscinomefile():
    print(" ==== file di testo da convertire in audio ===")
    for file in glob.glob("*.txt"):
        print(file)
    print(" =============================================")
    print()
    chiave = input("Quale file scegli per creare il file html con l'audio delle domande e delle risposte creato da Giovanni Gatto?")
    return chiave


filename = inseriscinomefile()

n = 0
html = "<script src=\"audio.js\"></script><script> audiojs.events.ready(function() {var as = audiojs.createAll(); }); </script>"
with open(filename + ".txt", 'r', encoding="utf-8") as file:
    for line in file.readlines():
        if line == "\n":
            pass
        elif line[-2] == "?":
            print(line)
            n += 1
            name = filename[:-4] + str(n) + ".mp3"
            html += "<h2><a href='" + name + "' onclick=javascript:mp3" + str(n) + ".innerHTML='ciao'>" + line + "</a></h2>"
            # html += "<audio id='speak'><source src='" + name + "' type='audio/mpeg' /></audio>"
            html += "<audio preload=\"auto\"> <source src='" + name + "''> </audio>"
            saveaudio(line, name)
        else:
            print(line)
            n += 1
            html += "<div id='mp3'" + str(n) + ">" + line + "</p>"
            name = filename[:-4] + str(n) + ".mp3"
            html += "<audio preload=\"auto\"> <source src='" + name + "''> </audio>"
            x = 1  # put this to 1 if you want to save audio
            saveaudio(line, name)

            # os.system(name)

with open(filename + ".html", "w", encoding='utf-8') as file:
    file.write(html)
os.system(filename + ".html")
