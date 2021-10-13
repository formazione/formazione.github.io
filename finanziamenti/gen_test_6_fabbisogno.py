import random
import os


tmp = "Calcola l'interesse su 10.000 € al tasso del 7% per 1 anno."

def genex():
	s = {
		"random_start": random.choice([
			"Trova il",
			"A quanto ammonta il",
			"Calcola il",
			"Calcolare il",
			"Trovare il",
			"Devi trovare il",
			"Fai il calcolo del"

			])
	}
	# valore delle merci
	merci = s["valore_merci"] = random.randrange(100, 1000, 100)
	mese_pag = random.randint(6,12)
	acquista = mese_pag - 2

	# data del pagament
	s["mese_pag"] = random.choice(["giugno", "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"])
	# data dell'acquisto
	s["mese_acquisto"] = random.choice([
		"gennaio", "febbraio", "marzo", "aprile", "maggio"
		])

	# Guadagn
	vend = s["percentuale_vendite"] = random.randrange(50, 80, 10)
	ric = s["perc_ricarico"] = random.randrange(25, 50, 10)
	costo_venduto = merci * vend / 100
	prezzo_venduto = costo_venduto + costo_venduto * ric / 100

	r = s["prezzo_venduto"] = str(prezzo_venduto)

	if "." in str(r):
		s["prezzo_venduto"] = str(prezzo_venduto) + " # " + str(prezzo_venduto).replace(".", ",")


	return s

def printex():
	s = genex()
	inp = """input("{random_start} valore delle merci acquistate il primo {mese_acquisto} al prezzo di {valore_merci} € delle quali il primo {mese_pag} si vende il {percentuale_vendite} % applicando un ricarico del {perc_ricarico} %.", "{prezzo_venduto}");""".format(**s)
	print(inp)
	return inp



def show():
	html = """
<style>
	.fontbig {
		font-size: 1.5em;
	}
</style>
<body oncontextmenu="return false;">
<script>

function check(casella, giusta, num){
	// the solutions are good both for low and capital letters

	if (giusta.includes(casella.value.split("#"))){
		casella.style.background = 'yellow';
		return casella.value;
	}
	else{
		casella.style.background = 'red';
	}
}

function print_it(parola){
	if (soluzioni.innerHTML.includes(parola)){
	}
	else {
    	soluzioni.innerHTML += " - " + parola;
	}
}

var countdom = 1;
function input(domanda, giusta){
	var dom_h2 = "<table style='background:#fcab41;'><td><p class='fontbig' style='color: blue'>" + countdom++ + " " + domanda;
	var part1 = dom_h2 + "<center>Prezzo delle merci vendute<input id='casella' class='fontbig' type=text class='t1' placeholder='?...' onchange=\\"if (check(this,'";
	part1 += giusta + "')){print_it(this.value)};\\" /></center></p></table>";
	document.write(part1);
	}
	

x = document.getElementsByClassName('t1');
for (i of x){
    i.value = "";
}

</script>
<h1>Fabbisogno 1</h1>

<script>
		"""
	print(html)
	for x in range(10):
		html += printex()
	print("</script>")
	html += "</script>"
	with open("fabbisogno1.html", "w") as file:
		file.write(html)
	os.startfile("fabbisogno1.html")

show()