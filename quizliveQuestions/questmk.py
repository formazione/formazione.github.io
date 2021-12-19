import os

text = """<!--
Tool for quizlive5

-->

1. [q1]
<input type="text" id="i1"><br><br><br>

2. [q1]
<input type="text" id="i2"><br><br><br>


3. [q1] 
<input type="text" id="i3"><br><br><br> 


4. [q1]
<input type="text" id="i4"><br><br><br>

5. [q1]
<input type="text" id="i5"><br><br><br>


6. [q1]
<input type="text" id="i6"><br><br><br>

7. [q1] 
<input type="text" id="i7"><br><br><br>


8. [q1]
<input type="text" id="i8"><br><br><br>


9. [q1]
<input type="text" id="i9"><br><br><br>


10. [q1]
<input type="text" id="i10"><br><br><br>

<p></p>
<button id="c1" onclick="inp1.value=i1.value+' ' + i2.value + ' ' + i3.value + ' ' + i4.value + ' ' + i5.value+ ' ' + i6.value+ ' ' + i7.value+ ' ' + i8.value+ ' ' + i9.value+ ' ' + i10.value">Invia risposte del test</button>

<p></p>
<input type="text" id="inp1">"""


questions = """Partita
Secondo la partita doppia dare e avere devono sempre essere ....
I conti finanziari si devono valutare?
In dare dei conti finanziari vanno (entrate o uscite)
In avere dei conti finanziari vanno
In dare dei conti economici vanno (costi o ricavi) ...
Il conto merci c/acquisti è economico o finanziario?
Il cassa  è economico o finanziario?
Il banca  è economico o finanziario?
Il automezzi è economico o finanziario?
Il crediti v/clienti è economico o finanziario?
""".splitlines()

# Put 1 if you want ommissis words without breaks
# 0 to put each question on new line with numbers
def get_var():
	import tkinter as tk
	from tkinter import simpledialog


	root= tk.Tk().withdraw()
	continuous = simpledialog.askstring(title="Senza break", prompt="Scrivi 1 se voui il testo di seguito")
	return continuous


continuous = get_var()
# continuous = 1
if continuous:
	text = text.replace("<br>", "")

titolo = questions[0]
for r in range(1, len(questions)):
	if continuous:
		text = text.replace(f"{r}. [q1]", questions[r], 1)
	else:
		text = text.replace("[q1]", questions[r], 1)

with open(f"{titolo}.html", "w") as file:
	file.write(text)

os.system(f"{titolo}.html")