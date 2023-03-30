#question generator
from random import choice, sample
italian = """
casa
tavolo
cucina
salotto
strada
auto
bicicletta
pallone
calcio
libro
quaderno
penna
matita
pennarello
tavolo
sedia
scarpa
pantaloni
camicia
cappello
berretto
orologio
telefonino
cintura
letto
armadio
""".splitlines()


french = """
home
table
Kitchen
living room
street
car
bicycle
ball
soccer
book
notebook
pen
pencil
marker
table
chair
shoe
trousers
Shirt
hat
cap
clock
mobile phone
belt
Bed
Wardrobe
""".splitlines()

names = []
for i,f in zip(italian,french):
	names.append(f"{i},{f}")

names.pop(0)


print(names)
def generate(nm):
	# print(nm)
	global qa
	# print(q)
	# print(a)

	qa2 = names.copy()
	q=[n.split(",")[0] for n in qa2]
	a=[n.split(",")[1] for n in qa2]
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

	print(question[0])
	for n in answer_choice:
		print(n)
	print()

qa = names.copy()
q=[n.split(",")[0] for n in qa]
a=[n.split(",")[1] for n in qa]
qa = [(n,a) for n,a in zip(q,a)]
for n in names:
	generate(qa)
	# print(qa)
