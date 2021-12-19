# in darm 2 ho fatto in modo che si possa usare l'apostrofo (codice 18-21)

import glob
import os
from random import choice
from tkinter import filedialog, simpledialog

# THE IMAGE SEEN IN THE QUIZ - ALWAYS THE SAME
imgRnd = """https://tuocoach.files.wordpress.com/2018/11/cambiamento-10.jpg?w=345&h=294
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
	with open("template_darm.html") as file:
		template = file.read()
	text_to_replace_in_template = """let quiz = [
{
	        "question"      :   "Quale articolo definisce il contratto?",
	        "image"         :   "https://tuocoach.files.wordpress.com/2018/11/cambiamento-10.jpg?w=345&h=294",
	        "choices"       :   ['1321 c.c.', '1322 c.c.', '1323 c.c.', '1324 c.c.'],
	        "correct"       :   "1321 c.c.",
	        "explanation"   :   "",
	    },
];"""
	
	js_questions = "" # will contain all the questions
	for d in qdic:
		js_questions += makeQ(d, qdic[d])
	js_questions = f"\nlet quiz = [{js_questions}];\n"
	htmlpage = template.replace(text_to_replace_in_template, js_questions)
	print("Inserite le domande")
	print("Creiamo il file:")
	# filename = f"{input('nome del file')}.html"
	filename = simpledialog.askstring("inserisci nome file", "Nome")
	print(filename)
	with open(filename + ".html", "w", encoding='utf-8') as file:
		file.write(htmlpage)
	print(os.getcwd())
	os.system(f"{filename}.html")
	# createfile(filename, htmlpage)

open_file() # chose the file with the questions and crete qdic
createDarm() # convert qdic in js, put in template and create file
