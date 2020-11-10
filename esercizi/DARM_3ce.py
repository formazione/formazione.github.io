# in darm 2 ho fatto in modo che si possa usare l'apostrofo (codice 18-21)

import glob
from random import choice
from createfile import createfile
from darm_start_3ce import *
from darm_end import *

imgRnd = """https://tuocoach.files.wordpress.com/2018/11/cambiamento-10.jpg?w=345&h=294
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
	#print(mklist(fn))


def createDarm():
	global htmlpage
	htmlpage += "quiz = ["
	for d in qdic:
		htmlpage += makeQ(d, qdic[d])
	htmlpage += endpage
	createfile(f"turismo_3ce.html",htmlpage)

menu()
createDarm()
