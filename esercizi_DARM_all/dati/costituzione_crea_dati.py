from random import shuffle, sample
import os

'''
This version
- gets the alternative questions randomly
- does


'''



alt1 = """...fondata sul lavoro#art.1
la repubblica, una e indivisibile, riconosce e promuove le autonomie locali#art. 5
tutela le minoranze linguistiche#art. 6
Stato e Chiesa... sono indipendenti e sovrani#art. 7
diritto al lavoro#art. 4
tutte le confessioni religiose sono ugualmente libere#art. 8
tutela il paesaggio#art. 9
si conforma alle norme del diritto internazionale#art. 10
diritti inviolabili#art. 2 
principio di uguaglianza#art. 3
verde bianco e rosso#art. 12
l'Italia ripudia la guerra#art. 11
il voto è personale#art. 48
tutti i cittadini hanno diritto di associarsi in partiti#art. 49
la difesa della patria è sacro dovere del cittadino#art. 52
Tutti sono tenuti a concorrere alle spese pubbliche in ragione della loro capacità contributiva#art. 53
Tutti i cittadini hanno il dovere di essere fedeli alla Repubblica#art. 54
La Repubblica tutela la salute#art. 32
La scuola è aperta a tutti.#art. 34
L'arte e la scienza sono libere e libero ne è l'insegnamento#art. 33
La Repubblica agevola ... la formazione della famiglia#art. 31
E` dovere e diritto dei genitori mantenere, istruire ed educare i figli#art. 30
La Repubblica riconosce i diritti della famiglia#art.29
Il Parlamento si compone della Camera dei deputati e del Senato della Repubblica.#art. 55
Il numero dei deputati è di quattrocento#art. 56
Il numero dei senatori elettivi è di duecento#art. 57
Sono eleggibili a senatori gli elettori che hanno compiuto il quarantesimo anno#art. 58
E` senatore di diritto e a vita, salvo rinunzia, chi è stato Presidente della Repubblica#art. 59"""

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
