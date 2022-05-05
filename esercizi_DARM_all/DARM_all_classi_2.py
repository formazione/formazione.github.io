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

Elenco fix
# problem_1			images from google



'''


imgRnd = """https://tuocoach.files.wordpress.com/2018/11/cambiamento-10.jpg?w=345&h=294
""".splitlines()

def makeQ(q, ch):
	''' takes q(uestions) and ch(answers) into the html str '''

			# problem_1 v.2 - 5.5.2021 #
	# images are random, can we make images 
	# to be loaded from google taking
	# the question as keyword, download them
	# into img folder and give the address to the
	# image key ?

	html = f"""{{
	        "question"      :   "{q}",
	        "image"         :   "{choice(imgRnd)}",
	        "choices"       :   {ch},
	        "correct"       :   "{ch[0]}",
	        "explanation"   :   "",
	    }},"""
	return html


qdic = {}
def mklist(filename) -> dict:
	""" -------------------------------------------------
	---------------------- mklist ------------------------
	Return a dictionary and a list of questions and aswers in a txt file where there is a question and answers for each line separated by an empty line for every group of question and answers ------------------------------------------
	-------------------------o---------------------------
	  -------------------------------------------------
	"""
	global qdic, classe
	flist = []
	# opens the file relative to a class and split it
	# into a LIST of lists of questions/answers into
	with open(f"{os.getcwd()}/dati/{classe}/{filename}", 'r', encoding='utf-8') as file:
		file = file.read()
		file = file.split("\n\n")
	# Append a list with question and answers for each string
	for eachstring in file:
		flist.append(eachstring.split("\n"))
	# get rid of empty line
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
	"""a menu to choose a file in the directory 'dati'"""
	global classe

	print("File di testo nella cartella: dati")
	print("------------------------------------")
	for number,eachfile in enumerate(glob.glob(f"dati\\{classe}/*.txt")):
		print(number, eachfile.split("\\")[-1])
	print("------------------------------------")
	file_number = int(input("Scegli il numero del file? > "))
	print(classe)
	path = f"{os.getcwd()}"
	fn = glob.glob(f"{path}/dati/{classe}/*.txt")
	print(fn)
	fn = fn[file_number].split("\\")[-1]
	print(fn)
	mklist(fn)
	return fn
	#print(mklist(fn))


def file_write(filename, content):
	with open(f"output/{filename}", "w", encoding="utf-8") as file:
		file.write(content)

def replace_js_title(filetext, filename):
	global classe

	filetext = filetext.replace("marketing.js", filename + ".js")
	filetext = filetext.replace("Percentuali e proporzioni", filename)
	filetext = filetext.replace("5ce2020_prova", filename)
	filetext = filetext.replace("listanomi5ce.js", f"listanomi{classe}.js")
	return filetext

def create_html(classe, filename):
	"""Substitute something in template3_3ce and create as new file with new name\
     .js contains the questions\
     .html contains the html code\
	"""
	filetext = open_template(f"template.html")
	filetext = replace_js_title(filetext, filename)
	file_write(f"{filename}{classe}" + ".html", filetext)
	os.startfile(f"{os.getcwd()}/output/{filename}{classe}" + ".html")


def open_template(filename):
	with open(filename) as file:
		filetext = file.read()
	return filetext



def create_domande_js(filename):

	domandejs = "quiz = ["
	for d in qdic:
		domandejs += makeQ(d, qdic[d])
	domandejs += "];"
	with open(f"output/{filename}.js", "w", encoding="utf-8") as file:
		file.write(domandejs)
	# os.startfile("domande.js")


def main():
	global classe

	if "output" not in os.listdir():
		os.mkdir("output")

	def classchooser(classi: str):
		# Sceglie il template da caricare con i nomi delle classi personalizzati
		classi = classi.split()
		print(*[x for x in enumerate(classi)])
		print("scegli classe :")
		classe = classi[int(input("Scegli la classe n. : "))]
		print(classe)
		return classe


	classe = classchooser("3ce 4ce 4ae 5ae 5ce")
	print(f"You choose {classe}")
	fn = menu()
	fn = fn.split("\\")[0]
	print(fn)
	# crea le domande dal file scelto
	create_domande_js(fn[:-4])
	# crea l'html con i nomi degli alunni e le domande scelte dal file
	create_html(
		classe,
		fn[:-4])
	# createDarm()

main()