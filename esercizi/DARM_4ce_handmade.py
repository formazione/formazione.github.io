# in darm 2 ho fatto in modo che si possa usare l'apostrofo (codice 18-21)

import glob
from random import choice
# from createfile import createfile
import os

'''

			Usa un template solo prova_marketing.html
			sostituisci marketing.js con il nome del file txt che
			usi per le domande (rendi la variabile filename globale)

			salva:
				- domande.js
				- file.html

'''


imgRnd = """imgs/ratei.png
imgs/ratei.png
""".splitlines()

def makeQ(q, ch):
	ch_html = "quiz = ["
	for r in ch:
		ch_html += "\"" + r + "\","
	ch_html += "]" 

	html = f"""{{
	        "question"      :   "{q}",
	        "image"         :   "{choice(imgRnd)}",
	        "choices"       :   {ch},
	        "correct"       :   "{ch[0]}",
	        "explanation"   :   "",
	    }},"""
	return html


qdic = {}
def mklist(filename):
	"Return a dictionary and a list of questions and aswers in a txt file where there is a question and answers for each line separated by an empty line for every group of question and answers"
	global qdic
	flist = []
	with open(filename, 'r', encoding='utf-8') as file:
		file = file.read()
		file = file.split("\n\n")
	for eachstring in file:
		flist.append(eachstring.split("\n"))
	for eachsublist in flist:
		for e in eachsublist:
		
		# avoid empty lines at the end
			if e == '':
				eachsublist.pop(eachsublist.index(e))
		# avoid empty lines at the end
		
		question = eachsublist[0]
		eachsublist.pop(0)
		qdic[question] = eachsublist
	return qdic


def menu():
	"a menu to choose a file in the directory 'dati'"
	print("File di testo nella cartella: dati")
	print("------------------------------------")
	for number,eachfile in enumerate(glob.glob("dati/*.txt")):
		print(number, eachfile.replace("dati\\",""))
	print("------------------------------------")
	file_number = int(input("Scegli il numero del file? > "))
	fn = glob.glob("dati/*.txt")[file_number]
	mklist(fn)
	return fn
	#print(mklist(fn))


def file_write(filename, content):
	with open(f"{filename}", "w", encoding="utf-8") as file:
		file.write(content)

def replace_js_title(filetext, filename):
	filetext = filetext.replace("marketing.js", filename + ".js")
	filetext = filetext.replace("Percentuali e proporzioni", filename)
	filetext = filetext.replace("5ce2020_prova", filename)
	return filetext

def create_html(filename):
	"Substitute something in template3_3ce and create as new file with new name\
     .js contains the questions\
     .html contains the html code\
	"
	filetext = open_template("template4_4ce.html")
	filetext = replace_js_title(filetext, filename)
	file_write(filename + ".html", filetext)
	os.startfile(filename + ".html")


def open_template(filename):
	with open(filename) as file:
		filetext = file.read()
	return filetext



def create_domande_js(filename):

	domandejs = "quiz = ["
	for d in qdic:
		domandejs += makeQ(d, qdic[d])
	domandejs += "];"
	with open(f"{filename}.js", "w", encoding="utf-8") as file:
		file.write(domandejs)
	# os.startfile("domande.js")



fn = menu()
fn = fn.split("\\")[1]
print(fn)
create_domande_js(fn[:-4])
create_html(fn[:-4])
# createDarm()
