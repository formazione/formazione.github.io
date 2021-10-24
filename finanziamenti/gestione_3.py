import random
import os

''' How to...

Go to the end end insert the questions like you see in lista_domande

you can put more possible answers using #

you can add a list of possible answer in the question with #

'''

def add_questions(lista_domande):
	''' creates a string with all call to input with questions and answer to be shown '''

	inp = ""
	for k in lista_domande:
		inp += "document.write('<h2>" + k + "</h2>');\n"
		for d in lista_domande[k]:
			if "^" in d[0]:
				print("found ^")
				address = d[0].split("^")[0]
				d[0] = d[0].replace(address+"^", "")
				# ===================== LINK IMG HTML CODE ===========
				address = f"<img src='{address}' width=200/><br>"
				d[0] = address + d[0]
			if "\\" in d[0]:
				d[0] = d[0].replace("\\", "<br>")
			if "#" in d[0]:
				question = d[0].split("#")[0]
				possible = d[0].split("#")[1:]
				possible = "[" + ",".join(possible) + "]"
				inp += f"""input("{question}<br>{possible}", "{d[1]}");\n"""
			else:
				inp += f"""input("{d[0]}", "{d[1]}");\n"""

	return inp


def start():

	style = """
	<style> 
	@import "button82.css";
		.fontbig {font-size: 1.5em; } 
		body, html {
			background: #ECEDEF;
			margin-left: 10%;
			margin-right: 10%;
			padding: 0; }
	</style>"""

	# hidemenu =  "<html oncontextmenu='return false;''>"
	hidemenu = ""

	check = hidemenu + """
		<script>
		const rightcolor = 'yellow'
		const wrongcolor = "red";
		let answers = new Array();
		function check(inp_text, giusta){
			let lista_esatte = giusta.split("#"); // right answers
			let user_input = inp_text.value.toString();       // user input
			if (lista_esatte.includes(user_input.toLowerCase()))
				{
				console.log("Giusto");
				inp_text.style.background = rightcolor; // turns yellow if right
				answers.push(inp_text.value.toString());
				console.log(answers);
				console.log(inp_text.value.toString());
				return inp_text.value;
				}
			else{
				inp_text.style.background = wrongcolor; // turn red if wrong
				};
			 }"""

	inputs = """ 
		var countdom = 1;

		function input(domanda, giusta){
			var dom_h2 = "<table style='background:#fcab41;'><td><p class='fontbig' style='color: blue'>" + countdom++ + " " + domanda;

			var part1 = dom_h2 + "<br><i style='color:red'>Answer and press return</i><br><input id='casella' class='fontbig' type=text class='t1' placeholder='?...' onchange=\\"if (check(this,'";
			
			part1 += giusta + "'));\\" style='text-align:right'/></center></p></table><br>";
			document.write(part1);
			}"""
		
	buttonfinal = """
			document.write(`<button class="button-82-pushable" role="button" onclick="check()">
			  <span class="button-82-shadow"></span>
			  <span class="button-82-edge"></span>
			  <span class="button-82-front text">Controlla le risposte</span>
			</button>`);



			"""
	end = "</script><h1>TITOLO</h1><script>"

	html = style + check + inputs

	# creates all the input("question", "answer") string
	html += add_questions(lista_domande)
	# close the script tag
	html += buttonfinal + end
	html += "</script>"
	html = html.replace("TITOLO", title)
	with open(f"{filename}.html", "w", encoding="utf-8") as file:
		file.write(html)
	os.startfile(f"{filename}.html")




# ===== Customize your quiz ================== >>>

'''
the sign '#' in the question puts a list of possible answers
the sign '#' in the answer puts alternative right answers

put a ^ after an image link to add an image in the question
'''
l1_imprese = "https://contrattidirete.registroimprese.it/reti/immagini/lalegge01.png"
l2_prestito = "https://www.lentepubblica.it/wp-content/uploads/2018/07/noipa-cedolino-speciale-rimborso-730.jpg"
l3_monetaria = "https://alleanzacattolica.org/wp-content/uploads/2020/11/denaro.jpg"

filename = "La banca"
title = "banca"
lista_domande = {

	"La banca":
	[
		[f"{l1_imprese}^Chi sono i principali soggetti in disavanzo?", "imprese"],
		[f"{l2_prestito}^La banca ha la sua principale attivita' nell'intermediazione ...c", "creditizia"],
		[f"{l3_monetaria}^La banca permette di utilizzare strumenti che sostituiscono il denaro come assegni, bonifici e carte di credito. Si tratta della funzione m....", "monetaria"]
	]


	}

# ==================== END customization =============== !!!

start()