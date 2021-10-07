import random

tmp = "Calcola l'interesse su 10.000 € al tasso del 7% per 1 anno."

def genex():
	s = {}
	C = s["Capitale"] = random.randrange(100, 1000, 100)
	r = s["tasso"] = random.randint(2,9)
	s["year_m_d"] = random.choice(["anni", "mesi", "giorni"])
	if s["year_m_d"] == "anni":
		t = s["tempo"] = random.randint(1, 5)
		s["interessi"] = C*r*t/100
	if s["year_m_d"] == "mesi":
		t = s["tempo"] = random.randint(1, 11)
		s["interessi"] = C*r*t/1200
	if s["year_m_d"] == "giorni":
		t = s["tempo"] = random.randint(1, 250)
		s["interessi"] = C*r*t/36500
	# s["sol"] = C*r*t/100
	s["final"] = ""
	if t > 1:
		s["final"] = "i"
	else:
		s["final"] = "o"
	if s["interessi"] == int(s["interessi"]):
		s["interessi"] = int(s["interessi"])
	else:
		s["interessi"] = round(s["interessi"])
	return s

def printex():
	s = genex()
	s["year_m_d"] = s["year_m_d"][:-1]
	print("dom(\"Calcola l'interesse su {Capitale} € al tasso del {tasso} % per {tempo} {year_m_d}{final}\", \"{interessi}\")".format(**s))


def show():
	for x in range(5):
		printex()

show()