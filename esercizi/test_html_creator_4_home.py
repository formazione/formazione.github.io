import glob
import os

'''


TEST A PAROLE OMESSE


Test realizzato da Giovanni Gatto. Clicca ctrl + b per generare un file html con il test. Ogni --parola-- sarà omessa.
"aiuto" : scrivendo aiuto verranno mostrate le prime tre lettere della risposta.


1. IMMETTERE UNA PAROLA OMESSA


    ========================
    ES:
    La capitale d'Italia è --Roma--
    <br>
    ========================

Nella versione attuale, ogni riga deve avere un --parola--, altrimenti aggiunge un Undefined ad una casella

'''


                    #-#-#      I N T R O D U Z I O N E    #-#-#


start = """
<style>
    body{
        font-size:2em;
        }

    input {
        font-size:24;
        display:inline;
        size:10;

    }


    h1, h2, h3 {

        background-color:coral;
        color: white;
    }

    p{
        color:blue;
        background-color:lightgreen;
        font-size:1.4em;
    }
</style>
<a href="https://formazione.github.io">Home</a>
<div id="score"><b>Score: </b></div>
"""


start += "<script>"




                    #-# TESTO CON LE PAROLE OMESSE TRA -- E -- (UNA PAROLA OMESSA PER RIGA)


                        # NOTA BENE !!!
# LA PRIMA RIGA è IL NOME DEL FILE HTML CHE CONTERRA' L'ESERCIZIO
#                   ||
#                   \/
testo = """stumenti_di_lavoro
<h2>strumenti di lavoro</h2>

<h3>Rispondi</h3>

Come si chiama il risultato di una divisione?
--rapporto--

L'uguaglianza di due rapporti si chiama
--proporzione--

Sappiamo che il primo e l'ultimo termine si chiamano:
--estremi--

Il secondo e il terzo termine della proporzione si chiamano:
--medi--

"""

testo = testo.replace("'", "`")

splitsign = "--"


print(start)
content = ""

# content will contain all the input(.......) that will create the omitted text input widgets
testo = testo.splitlines()
filename = testo[0]
for n, line in enumerate(testo[1:]):
    # If the line is empty it skips
    if line == "" or line == "\n":
        pass
    # if there is no --
    elif "--" not in line:
        content += f"\ndocument.write('<p>{line}</p>');\n"
    else:
        dom = line.split(splitsign)
        if line[0] == line[1] == "-":
            dom[0] = " " + line.split(splitsign)[0]
        dom_start = dom[0]
        giusta = dom[1]
        dom_end = dom[2]
        if dom[0][0] == "#":
            tipodirisposta = "guessWhat"
            dom[0] = dom[0].replace("#", "")
        else:
            tipodirisposta = "input"
        content += tipodirisposta + "(\"" + dom_start + "\", \"" + giusta.strip() + "\",\"" + dom_end.strip() + "\");\n"


end = """document.write("</p>");\naddsol();"""

print(content + end)

end = "</script>"

script = """ <div id="soluzioni">Soluzioni: </div><script>
let punteggio = 0;

// ==================== check ======================

function check(casella, giusta, num){
    giusta = giusta.toLowerCase();
    casella.value = casella.value.toLowerCase();
        if (casella.value == 'aiuto'){
        if (casella.value.length >= 3){
        casella.value = giusta[0]+giusta[1]+ giusta[2]
        }
    }
    else{
    if (casella.value == giusta){
        casella.style.background = 'yellow';
        casella.style.color = 'blue';
        punteggio +=1
        score.innerHTML = "<b>Score: " + punteggio + "<b>";
        document.getElementById(casella.id).readOnly = true;
        return casella.value.includes(giusta);
    }
    else{
        casella.style.background = 'red';
    }

}
}


// ===================== checkWhat =======

function checkWhat(casella, giusta, num){
    giusta = giusta.toLowerCase();
    casella.value = casella.value.toLowerCase();
    if (casella.value == 'aiuto'){
        if (casella.value.length >= 3){
        casella.value = giusta[0]+giusta[1]+ giusta[2]
        }
    }
    else {
    for (r of giusta.split(" ")){
        if (casella.value == r){
            casella.style.background = 'yellow';
            return casella.value.includes(giusta);
        }
        else{
        casella.style.background = 'red';
    }
    }
}

}

// ============================ print_it ============

function print_it(parola){
    if (soluzioni.innerHTML.includes(parola)){
    }
    else {
        soluzioni.innerHTML += " - " + parola;
    }
}


var sol = [];
    var countdom = 0;


// ==================== input ====================

var num = 0;
function input(dom_s, giusta, dom_e){ 
    sol.push(giusta); 
    var part1 = dom_s + "<input type=text class='t1' placeholder='"
    part1 += giusta[0] + "....' onchange=\\"if (check(this,'";
    part1 += giusta + "')){print_it(this.value)};\\" /><td>" + dom_e
    document.write(part1);
}


// ==================== guessWhat =====================

    function guessWhat(dom_s, giusta, dom_e){
        dom_s = dom_s.replace("#"," ");
        sol.push(giusta);
        var part1 = dom_s + "<input type=text class='t1' placeholder='"
        part1 += giusta[0] + "....' onchange=\\"if (checkWhat(this,'";
        part1 += giusta + "')){print_it(this.value)};\\" /><td>" + dom_e
        document.write(part1);
    }


// ============================= addsol ==================

function addsol(){
    //document.write("<div id='soluzioni'>Suggerimenti: </div>");
    //sol.sort();
    console.log("Before loop");
    }

function mostra_soluzioni(){
    console.log(sol);
    for (s of sol){
        console.log(sol);
    }
}

</script>


"""

text = script + start + content + end
filename = f"{filename}.html"
with open(filename, "w", encoding="utf-8") as file:
    file.write(text)
#print(text)
os.startfile(filename)