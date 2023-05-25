#question generator
from random import choice, sample
names = """
2+2=4
2+3=5
3+3=6
4+3=7
5+5=10
5+3=8
1+1=2
1+0=1
9+3=12
8+2=10
""".splitlines()[1:]

def generate(nm):
	# print(nm)
	global qa
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

	print(question[0])
	for n in answer_choice:
		print(n)
	print()


qa = names.copy()
q=[n.split("=")[0] for n in qa]
a=[n.split("=")[1] for n in qa]
qa = [(n,a) for n,a in zip(q,a)]
for n in names:
	generate(qa)
	# print(qa)
