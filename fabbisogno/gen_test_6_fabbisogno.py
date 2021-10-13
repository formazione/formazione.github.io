import random

tmp = "Calcola l'interesse su 10.000 € al tasso del 7% per 1 anno."

def genex():
	s = {}
	# valore delle merci
	merci = s["valore_merci"] = random.randrange(100, 1000, 100)
	data_pag = random.randint(6,12)
	acquista = data_pag - 2

	# data del pagamento
	s["data_pag"] = f"1.{data_pag}"
	# data dell'acquisto
	s["data_acq"] = f"1.{acquista}"

	# Guadagn
	vend = s["percentuale_vendite"] = random.randrange(50, 80, 10)
	ric = s["perc_ricarico"] = random.randrange(25, 50, 10)
	costo_venduto = merci * vend / 100
	prezzo_venduto = costo_venduto + costo_venduto * ric / 100

	r = s["prezzo_venduto"] = prezzo_venduto


	return s

def printex():
	s = genex()
	print("""input("Calcola il valore delle merci vendute per sapere se si otterranno entrate superiori alle uscite entro la data di pagamento delle fatture di acquisto sapendo che: un impresa il giorno {data_acq} acquista merci per {valore_merci} € da pagare entro il {data_pag} sapendo che venderà con un ricarico di {perc_ricarico} % entro il giorno {data_pag} il {percentuale_vendite} % delle merci acquistate.", {prezzo_venduto});""".format(**s))



def show():
	print("""
<style>
	.fontbig {
		font-size: 1.5em;
	}
</style>
<body oncontextmenu="return false;">
<script>

function check(casella, giusta, num){
	// the solutions are good both for low and capital letters
	if (giusta.includes(casella.value.toLowerCase())){
		casella.style.background = 'yellow';
		return casella.value.includes(giusta);
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
	var part1 = dom_h2 + "<center><input id='casella' class='fontbig' type=text class='t1' placeholder='?...' onchange=\\"if (check(this,'";
	part1 += giusta + "')){print_it(this.value)};\\" /></center></p></table>";
	document.write(part1);
	}
	

x = document.getElementsByClassName('t1');
for (i of x){
    i.value = "";
}

</script><script>
		""")
	for x in range(10):
		printex()
	print("</script>")
show()