# in darm 2 ho fatto in modo che si possa usare l'apostrofo (codice 18-21)

import glob
import os
from random import choice
# from createfile import createfile
from darm_start import *
from darm_end import *
from tkinter import filedialog, simpledialog

# THE IMAGE SEEN IN THE QUIZ - ALWAYS THE SAME
imgRnd = """https://lh3.googleusercontent.com/proxy/i_N9SY1HspoCodlP807w3IztBbgtmZPyafPSYo_NcDd-kkzLiv5rXPfHeXCbLT447CsMt2pbMcuSAjc-hnQdLY-2n9AoGsJXEXWLi7btJZjH1DNBNHxlAS7WjQ
""".splitlines()

def makeQ(q,ch):
	''' PASS THE LIST FROM THE TEXT FILE WITH THE QUESTION TO CREATE THE RIGHT
		JAVASCRIPT CODE FOR THE QUESTIONS IN THE HTML FILE
	'''
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
def open_file():
	'''Return a dictionary and a list of questions and aswers in a txt file where there is a question and answers for each line separated by an empty line for every group of question and answers'''
	global qdic
	
	# CHOOSE FILE
	filename = filedialog.askopenfilename(initialdir=".")
	flist = []
	# OPENS FILE CHOSEN AND APPEND THE QUESTIONS
	with open(filename, 'r', encoding='utf-8') as file:
		file = file.read()
		file = file.split("\n\n")
	for eachstring in file:
		flist.append(eachstring.split("\n"))
	# CREATE THE QDIC TO SUBMIT TO CREATEDARM FOR THE RIGHT DATA SET
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


def createDarm():
	''' AFTER CREATED QDIC IN OPEN_FILE() IT CREATES THE HTML CODE 
		WIHT START + QUESTIONS + END
	'''
	global htmlpage
	for d in qdic:
		htmlpage += makeQ(d, qdic[d])
	htmlpage += endpage
	# filename = f"{input('nome del file')}.html"
	filename = simpledialog.askstring("inserisci nome file", "Nome")
	with open(filename + ".html", "w", encoding='utf-8') as file:
		file.write(htmlpage)
	os.system(f"start {filename}")
	# createfile(filename, htmlpage)

open_file()
createDarm()
