#question generator
from random import choice, sample
from math import prod
import os

def split(s: str):
	return [int(x) for x in s.split(" ")]

tabellina = ""
def gen_tabelline(x: int):
	''' autogenerate questions string to copy in names '''
	global tabellina

	adata = x # la tabellina del ... x
	bdata = split("1 2 3 4 5 6 7 8 9 10") # multiply for this
	for data in bdata:
		# print(f"{adata} x {data} = {adata*data}")
		tabellina += f"{adata} x {data} = {adata*data}\n"

gen_tabelline(3) # call function that generates strings with tabelline
# use genex to generate this
names = tabellina.splitlines()

text = ""
def savetext(x):
	global text, answer_choice
	print(answer_choice[-1])
	text += x
	text += "\n"

def generate(nm):
	# print(nm)
	global qa, answer_choice
	# print(q)
	# print(a)

	qa2 = names.copy()
	q=[n.split("=")[0] for n in qa2]
	a=[n.split("=")[1] for n in qa2]
	qa2 = [(n,a) for n,a in zip(q,a)]

	# print(qa)
	question = choice(qa)
	# print(f"{question=}")
	right_answer = question
	# right_answer = question[1]
	# print(question)
	qa2.pop(qa2.index(question))
	qa.pop(qa.index(question))
	answers = [n for n in sample(qa2,k=3)]
	answers.insert(0, right_answer)
	# print(answers)
	answer_choice = [n[1] for n in answers]
	# print(answer_choice)
	# print(question[0])
	savetext(question[0])
	for n in answer_choice:
		# print(n)
		savetext(n)

	# print()




qa = names.copy()
q=[n.split("=")[0] for n in qa]
a=[n.split("=")[1] for n in qa]
qa = [(n,a) for n,a in zip(q,a)]
# print(names) # names are the strings with "3x1 = 3"
# print(qa) # qa are the tuple with ('3x1','3')
for n in names:
	generate(qa)
	if n != names[-1]:
		savetext("")
	# print(qa)

fname = "../dati/filegenerato.txt"
def savefile(t):
	global fname
	with open(fname, "w") as file:
		file.write(t[:-1])


os.system(f"start {fname}")

savefile(text)
