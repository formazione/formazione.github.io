from random import shuffle
html1 = """<div style="background-color:lightblue">"""

n = 0  # counter


def quest(domanda_p1, domanda_p2, r1, r2, r3, r4):
    global n
    n = str(n)
    risposta_esatta = r1
    lista_risposte = [r1, r2, r3, r4]
    shuffle(lista_risposte)
    r1, r2, r3, r4 = lista_risposte
    testo += """<h1>""" + domanda_p1 + """ <u><span id='a""" + n + """'>______</span></u> """ + domanda_p2 + """</h1><br>
<form id="d""" + n + """">
<input type="radio" name="choice" value='""" + r1 + """'> """ + r1 + """
<input type="radio" name="choice" value='""" + r2 + """'> """ + r2 + """
<input type="radio" name="choice" value='""" + r3 + """'> """ + r3 + """
<input type="radio" name="choice" value='""" + r4 + """'> """ + r4 + """
<br>
<input type="submit" value="submit" onclick="validate(choice.value, '""" + risposta_esatta + """', 'd""" + n + """','a""" + n + """')">
</form>
</div>"""
    n = int(n)
    n += 1


code = """<script>
var validate = function(valore, rightanswer, form, span) {

var formname = document.getElementById(form)
var spanname = document.getElementById(span)

    spanname.innerHTML = rightanswer;

if (valore == rightanswer) {
    formname.innerHTML ="<div style='background-color:lightgreen'><h1>Bravo! La risposta era: " + rightanswer + "</h1></div>";
}
else {

    formname.innerHTML ="<div style='background-color:pink'><h1>Sbagliato! La risposta era: " + rightanswer + "</h1></div>";
}
};
</script>"""

with open("prova_quiz6.html", "w", encoding="utf-8") as file:
    testo = html1
    with open("test_es1.txt", "r", encoding="utf-8") as dati:
        content = dati.readlines()
        for x in range(0, len(content), 4):
            print(content[x])
            line = content[x]
            quest(line, "", "", "", "", "")

    testo += code
    file.write(testo)
