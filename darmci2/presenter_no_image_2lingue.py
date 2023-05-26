# in darm 2 ho fatto in modo che si possa usare l'apostrofo (codice 18-21)

import glob
from random import choice
from scripts.createfile import createfile
from scripts.darm_start import *
from scripts.darm_end import *
import tkinter as tk
import requests
from bs4 import BeautifulSoup

''' darmci2 (Domande A Risposta Multipla Con Immagini 2)

In this version 2, if in the text there is a word after #
this will be the image to put in the question, the words 
in asteriscs will not be displayed

example
Qual è la capitale d'Italia? #colosseo

'''

def imglink(word):
    ''' lnk to first img in google src '''
    query = word  # the search query you want to make
    url = f"https://www.google.com/search?q={query}&tbm=isch"  # the URL of the search result page

    response = requests.get(url)  # make a GET request to the URL
    soup = BeautifulSoup(response.text, "html.parser")  # parse the HTML content with BeautifulSoup

    # find the first image link by searching for the appropriate tag and attribute
    img_tag = soup.find("img", {"class": "yWs4tf"})

    if img_tag is not None:
        img_link = img_tag.get("src")
        print(img_link)  # print the first image link
        return img_link
    else:
        print("No image found on the page.")
# print(soup.prettify())


def imglink(word):
	return ""

# imgRnd = """https://tuocoach.files.wordpress.com/2018/11/cambiamento-10.jpg?w=345&h=294
""".splitlines()
"""



imgRnd = imglink("cat")

def makeQ(q,ch):
	ch_html = "["
	for r in ch:
		ch_html += "\"" + r + "\","
	ch_html += "]" 

	html = f"""{{
	        "question"      :   "{q}",
	        "image"         :   "{imglink(q)}",
	        "choices"       :   {ch},
	        "correct"       :   "{ch[0]}",
	        "explanation"   :   "",
	    }},"""
	return html

def makeQ2(q,ch,im):
	ch_html = "["
	for r in ch:
		ch_html += "\"" + r + "\","
	ch_html += "]" 

	html = f"""{{
	        "question"      :   "{q}",
	        "image"         :   "{imglink(im)}",
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



def show_exercize(num_es):
	''' after the input, the exercize appears '''
	fn = glob.glob("dati/*.txt")[int(num_es)]
	mklist(fn)
	root.destroy()


def assign_e():
	global e, e3, entry2, entry3

	e = entry2.get()
	e3 = entry3.get()
	print(e)
	print(e3)


root = tk.Tk() # create the window
def menu():
	"a menu to choose a file in the directory 'dati'"
	global e, e3, entry, entry2, entry3

	root.geometry("400x700")

	files = ""
	for number,eachfile in enumerate(glob.glob("dati/*.txt")):
		files += f"{number}. {eachfile}\n"
	

	# lista dei files
	lablist = tk.Label(root, text=files)
	lablist.pack()
	lab = tk.Label(root, #etichetta con la scritta seguente
		text="Inserisci il numero dell'esercizio che vuoi vedere",
		bg="yellow")
	lab.pack()

	# [____________]  input
	entry = tk.Entry(root)
	entry.pack()
	entry.focus()
	entry.bind("<Return>", lambda x: show_exercize(entry.get()))
	print(entry.get())


	'''
				scegli lingua delle risposte
					[it]
	'''

	# scelta seconda lingua ---------------------------------
	lab3 = tk.Label(root, text="Scegli lingua delle domande")
	lab3.pack()
	entry3 = tk.Entry(root)
	entry3.insert(tk.END, "it")
	entry3.bind("<Return>", lambda x: assign_e())
	print(entry3.get())
	e3 = entry3.get()
	entry3.pack()
	# -----------------------------------------> 185


	
	# scelta seconda lingua ---------------------------------
	lab2 = tk.Label(root, text="Scegli lingua delle risposte")
	lab2.pack()
	entry2 = tk.Entry(root)
	entry2.insert(tk.END, "it")
	entry2.bind("<Return>", lambda x: assign_e())
	print(entry2.get())
	e = entry2.get()
	entry2.pack()
	# -----------------------------------------> 185



	root.mainloop() # create the main loop

	# vecchio codice con input nelka command line interface
	# print("File di testo nella cartella: dati")
	# print("------------------------------------")
	# for number,eachfile in enumerate(glob.glob("dati/*.txt")):
	# 	print(number, eachfile.replace("dati\\",""))
	# print("------------------------------------")
	# file_number = int(input("Scegli il numero del file? > "))
	# fn = glob.glob("dati/*.txt")[file_number]


	#print(mklist(fn))


def createDarm():
	''' incolla htmlpage, le domande e endpage sostituendo lingua risposte '''
	global htmlpage, e, endpage


	for d in qdic:
		if "#" in d:
			print(d)
			dom,im = d.split("#")
			htmlpage += makeQ2(dom,qdic[d],im)
		else:
			print(d)
			htmlpage += makeQ(d,qdic[d])
	# SOSTITUZIONE DELLA LINGUA DELLE RISPOSTE QUI (da 146)
	endpage = endpage.replace("fr", e)
	endpage = endpage.replace("it", e3)
	htmlpage += endpage
	createfile("cambia_nome.html",htmlpage)

menu()
createDarm()
