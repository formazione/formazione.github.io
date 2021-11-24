import os

filename = "template.html"
with open(filename) as file:
	file = file.read()

'''
       "Chirico",
        "Cona",
        "Dagosto",
        "Dinola",
        "Filosa",
        "Mariosa",
        "Mazzeo",
        "Merola",
        "Pandullo",
        "Paolino",
        "Papa",
        "Petrone",
        "Ruggiero",
        "Savino",
        "Volpe"

    "balbi",
    "bertolini",
    "cuda",
    "divivo",
    "iuliano",
    "lapastina",
    "lakrad",
    "maffia",
    "mercanti",
    "nese",
    "niglio",
    "pica",
    "spinelli"
'''

classe = [
        "Breglia",
        "Cammarano_D",
        "Cammarano_N",
        "Costantini",
        "Del Verme,",
        "Esposito",
        "Fontana",
        "Garofalo",
        "Giordano",
        "Grimaldi",
        "Lista",
        "Malzone",
        "Mandia",
        "Marchesani",
        "Musto",
        "Ruocco",
        "Santoro",
        "Scola_M",
        "SCOLA_V",

]


html = """
<style>

	

body, table, button {

  font-size: 1em;
}

.btn.btn-warning.btn-lg {
  background:pink;
  color:red;
}
.btn.btn-info.btn-lg {
  background:cyan;
  color:blue;
}

ul {font-size: 1em;}
i {font-size : 1em;}
p { font-size: 1em; }
td {font-size: 1.5em;}
table {
    border-collapse: collapse;
    width: 50%;
}

th, td {
    text-align: left;
    padding: 8px;
}

tr:nth-child(even){background-color: coral; color: white;}
tr:nth-child(odd){background-color: navy; color: white;}

	
</style>


<body>
<!-- 
domanda.insegnante c'è la mia domanda
5AE ci sono le risposte degli alunni
5ae_2020_2021 ci sono i punteggi degli alunni

 -->

<script src="https://www.gstatic.com/firebasejs/4.10.1/firebase.js"></script>
<script>
  var config = {
    apiKey: "AIzaSyDp-mWaWEI07pIdRUhi6vA-salEMRWz4hw",
    authDomain: "quiz-e5e5a.firebaseapp.com",
    databaseURL: "https://quiz-e5e5a.firebaseio.com/",
    projectId: "quiz-e5e5a",
    storageBucket: "quiz-e5e5a.appspot.com",
    messagingSenderId: "901845403492"
  };
  firebase.initializeApp(config);
  var database = firebase.database()
</script>
<h1>5AE 2021 202 Console Insegnante</h1>

Risposta:<i id="domanda_insegnante"></i>
<!-- domanda insegnante -->
<input type="text" class="inp1" onchange="dbdomanda.set(this.value)">
<script>
var domanda_insegnante = document.getElementById("domanda_insegnante");
var dbdomanda = firebase.database().ref().child("domanda").child("insegnante");
dbdomanda.on("value", snap => domanda_insegnante.innerText = snap.val());
dbdomanda.on("value", snap => inp1.value = snap.val())

</script>

<div id="div1" class="w3-main" style="margin-left:50px">
<table class="table-bordered">

"""

console = """
<!-- musto copia e cambia tutti i musto col nuovo nome -->
<td>
<button type="button" class="btn btn-warning btn-lg" onclick="dbRefmusto.set(--nmusto)"> - </button><button type="button" class="btn btn-info btn-lg" onclick="dbRefmusto.set(++nmusto)"> + </button>musto<td>
<!-- TESTO CHE MOSTRA LA RISPOSTA DI MANDIA E IL SUO PUNTEGGIO -->
Risposta:<i id="risposta_musto"></i>
Punti: <i id="h1alunnomusto"></i></p>
<!--               TASTI PER ASSEGNARE I PUNTI E VISUALIZZAZIONE RISPOSTA MANDIA -->
<script>
var h1alunnomusto = document.getElementById("h1alunnomusto");
// VEDI IL PUNTEGGIO nel child Mandia di 5ae_2021_2022 (Punteggio assegnato da me)
var dbRefmusto = firebase.database().ref().child("4ae_2021_2022").child("musto");
dbRefmusto.on("value", snap => h1alunnomusto.innerText = snap.val()); // mostra il valore di n1
// AGGIORNA PUNTEGGIO
dbRefmusto.on("value", snap => nmusto = snap.val()) // Cambia il valore della variabile n1
// VEDI IL PUNTEGGIO nel child Mandia di 5AE (sua risposta)
var i_risposta_musto = document.getElementById("risposta_musto");
var db_risposta_musto = firebase.database().ref().child("4AE").child("musto");
db_risposta_musto.on("value", snap => i_risposta_musto.innerText = snap.val());
db_risposta_musto.on("value", snap => n_musto = snap.val())</script>
<tr>
<!-- fine lista -->

"""


for alunno in classe:
	# create file for single pupil
	file1 = file.replace("musto", alunno)
	with open(alunno + ".html", "w") as newfile:
		newfile.write(file1)

	# create html for the console.html file
	console2 = console.replace("musto", alunno)
	print(alunno)
	html += console2
html += """
</table>
</div>
"""
with open("copia_in_console.html", "w") as newfileconsole:
	newfileconsole.write(html)

os.startfile("copia_in_console.html")


for alunni in classe:
	address = "https://formazione.github.io/quiz4ae/" + alunni + ".html"
	print(address)
	print()


for alunni in classe:
	address = "https://formazione.github.io/quiz4ae/" + alunni + ".html"
	print("<a href='" + address + "'>" + alunni + "</a><br>")
	print()