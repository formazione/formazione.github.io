# in darm 2 ho fatto in modo che si possa usare l'apostrofo (codice 18-21)

import glob
from random import choice
from createfile import createfile
from darm_start import *
from darm_end import *

imgRnd = """https://tuocoach.files.wordpress.com/2018/11/cambiamento-10.jpg?w=345&h=294
""".splitlines()

def makeQ(q,ch):
	ch_html = "["
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
	"Opens the filename (from user choice see menu())\
	splits each empty line = \n \n \
	\
	"
	global qdic
	flist = []
	def openfile(filename):
		"Read text in file and split for empty lines"
		with open(filename, 'r', encoding='utf-8') as file:
			file = file.read()
			file = file.split("\n\n")
		return file

	def create_dic(listquestions):
		for eachstring in listofquestions:
			flist.append(eachstring.split("\n"))
		for eachsublist in flist:
			for e in eachsublist:
				if e == '':
					eachsublist.pop(eachsublist.index(e))
			question = eachsublist[0]
			eachsublist.pop(0)
			qdic[question] = eachsublist
		return qdic

	listofquestions = openfile(filename)
	qdic = create_dic(listofquestions)
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
	for d in qdic:
		htmlpage += makeQ(d, qdic[d])
	htmlpage += endpage
	createfile("paste_in_darm.html",htmlpage)

menu()
createDarm()
