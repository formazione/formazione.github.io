from random import shuffle, sample
import os

'''
This version
- gets the alternative questions randomly
- does


'''



alt1 = """La Repubblica tutela il lavoro in tutte le sue forme ed applicazioni.#art. 35
Il lavoratore ha diritto ad una retribuzione proporzionata...#art.36
La donna lavoratrice ha gli stessi diritti#art.37
Ogni cittadino inabile al lavoro e sprovvisto dei mezzi necessari per vivere#art. 38
ha diritto al mantenimento e all’assistenza sociale.#art. 38
La libertà personale è inviolabile.#art.13
Il domicilio è inviolabile.#art.14
La libertà e la segretezza della corrispondenza e di ogni altra forma di comunicazione sono inviolabili.#art.15
Ogni cittadino può circolare e soggiornare liberamente#art.16
Tutti hanno diritto di manifestare liberamente il proprio pensiero#art. 21
L’organizzazione sindacale è libera.#ar. 39
L’iniziativa economica privata è libera.#art. 41
Sono elettori tutti i cittadini...#art.48
Tutti i cittadini hanno diritto di associarsi liberamente in partiti#art. 49"""

alt1 = alt1.splitlines()
print(f"Domande: {len(alt1)}")
shuffle(alt1)
qnum = len(alt1)

sol = alt1.copy()
questions = []
answers = []
for q in alt1:
	q, a = q.split("#")
	questions.append(q)
	answers.append(a)

qna = []
lettsol = []
letters = "abcd"
for n in range(qnum):
	a1 = sol[n].split("#")[1]
	pos = answers.index(a1)
	answers.pop(pos)
	# shuffle(answers)
	a2, a3, a4 = sample(answers, 3)
	qq = f"Quale articolo contiene... <b>'{questions[n]}'</b>?"
	x = [a1, a2, a3, a4]
	# shuffle(x)
	right = x.index(a1)
	lettsol.append(letters[right])
	qna.append([qq, x])
	answers.insert(pos, a1)
# print(*qna, sep="\n")


def lprint(x, br=0):
	global text
	if br:
		text += "<br>"
	text += x + "<br>"

# Print the questions and answers randomized
text = ""
counter = 0
qcount = 0
for q in qna:
	q, a = q

	# PRINT QUESTION 1. What.... ?
	qcount += 1
	plaintext = q.replace("<b>","")
	plaintext = plaintext.replace("</b>","")
	print(plaintext)
	# q = q.replace(q, f"<b>{q}</b>")
	# q = q.replace(questions[qcount-1], f"<u>{questions[qcount-1]}</u>")
	lprint(f"{q}", br=1)

	# PRINT MULTIPLE CHOICE a) ..... b) .....
	for ans in a:
		print(ans)
		lprint(ans)
		counter += 1
	counter = 0
	print()
	text += ""

# Print the solutions at the end
print("Solutions")
lprint("Solutions", br=1)
counter = 0
for ss in sol:
	q, s = ss.split("#")
	print(f"[{lettsol[counter]}]", q, s)
	lprint(f"[{lettsol[counter]}]{q} {s}")
	counter += 1
print("----")

# with open("mc.html", "w") as file:
# 	file.write(text)
# os.startfile("mc.html")
