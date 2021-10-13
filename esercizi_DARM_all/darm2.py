# in darm 2 ho fatto in modo che si possa usare l'apostrofo (codice 18-21)

import glob
from random import choice
# from createfile import createfile
import os

'''

			It use the template.html
			then replace it with the questions
			and the link to listanomi for the different classes
			the questions are saved in a separate js file

'''


imgRnd = """https://tuocoach.files.wordpress.com/2018/11/cambiamento-10.jpg?w=345&h=294
""".splitlines()

def makeQ(q, ch):
	''' creates the question to be replaced in the template.html '''
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
def mklist(filename: str) -> dict:
	''' Return a dictionary with key=question value=answers '''
	
	global qdic, classe
	flist = [] # gets all question and aswers as an item of the list splitting where \n\n
	filepath = f"{os.getcwd()}/dati/{classe}/{filename}"
	with open(f"{filepath}", 'r', encoding='utf-8') as file:
		file = file.read()
		file = file.split("\n\n") # here is the split with \n\n
	# file is a list with "q\nr1\nr2\nr3\nr3\n"
	for eachstring in file:
		# flist now has a list with items that are lists with 4 elements: q, r, r, r, r
		flist.append(eachstring.split("\n"))
	# for every list [q,r,r,r] in flist
	for eachsublist in flist:
		# for every item q r r r r in each [q,r,r,r,r]
		for e in eachsublist:
		# avoid empty lines at the end
			if e == '':
				eachsublist.pop(eachsublist.index(e))
		# avoid empty lines at the end
		# gets the question in the variable question and then pop it
		question = eachsublist[0]
		eachsublist.pop(0)
		qdic[question] = eachsublist # puts the answer in the dic key=question value=answers
	return qdic


def menu():
	global classe

	"a menu to choose a file in the directory 'dati'"
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
	''' Changing the html code for the test to add questions and change students names and title '''
	global classe

	# the file with the questions
	filetext = filetext.replace("marketing.js", filename + ".js")
	# the title of the quiz
	filetext = filetext.replace("Percentuali e proporzioni", filename)
	# the main file I think, the html file
	filetext = filetext.replace("5ce2020_prova", filename)
	# the file with the names of the students
	filetext = filetext.replace("listanomi5ce.js", f"listanomi{classe}.js")
	return filetext


def create_html(classe, filename):
	"Substitute something in template3_3ce and create as new file with new name\
     .js contains the questions\
     .html contains the html code\
	"
	filetext = open_template(f"template.html")
	filetext = replace_js_title(filetext, filename)
	file_write(filename + ".html", filetext)
	os.startfile(f"{os.getcwd()}/output/{filename}" + ".html")


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