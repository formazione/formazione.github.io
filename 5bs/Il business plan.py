# -*- encoding: utf-8 -*-
import os


def htmlbase(*func):
    def page():
        for f in func:
            print(f())
    return page


def head():
    "This goes into the head"
    return """</html>
<head>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script></head>"""


class DivButtons:
    collector = {}

    def __init__(self, title, parag=""):
        self.title = title
        self.parag = parag
        self.inner = ""
        self.buttons()
        DivButtons.collector[self.title] = self

    def buttons(self):
        return """<div class="container">
        <h2>""" + self.title + """</h2>
            <p>""" + self.parag + """</p>
                """ + \
            self.inner \
            + """
        </div>
    """

    def add_parag(self, content):
        self.parag += "<p>" + content + "</p>"

    def add_list(self, lista):
        "* after the : and # after ,"
        lista = lista.split("*")
        self.parag += "<ul><b>" + lista[0] + "</b>"
        for items in lista[1].split("#"):
            if "(" in items:
                items = items.replace("(", "</b>(<i>").replace(")", "</i>)</b>")
            self.parag += "<li><b>" + items + "</b></li>"
        self.parag += "</ul></p>"

    def add_button(self, caption):
        self.innerbody(self.buttonround(caption))

    def buttonround(self, caption):
        return("""<button type="button" class="btn btn-success">""" + caption + """</button> """)

    def buttonquare(self):
        return("""<button type="button" class="btn btn-default">Rounded corners</button>""")

    def innerbody(self, newbutton):
        "This is the collection of elements into the body"
        self.inner += newbutton
        return self.inner


def end():
    return "\n</html>"


# PRIMA PARTE


def print_at_console():
    testo = head()
    for k, v in DivButtons.collector.items():
        testo += v.buttons()
    testo += end()
    print(testo)
# ===== FINE =====


def create_html_file():
    with open("htmlfile.html", 'w', encoding='utf-8') as file:
        testo = head()
        for k, v in DivButtons.collector.items():
            testo += v.buttons()
        testo += end()
        file.write(testo)
    os.system("htmlfile.html")


# SECONDA PARTE

class Book:
    def __init__(self):
        self.parti()

    def parti(self):

        # Introduzione
        div0 = DivButtons("Il business plan")
        div0.add_parag("È il documento che consente di valutare un progetto imprenditoriale.")
        div0.add_list("È formato da tre parti:* la sintesi,# l'esposizione del progetto con il marketing plan,# la valutazione del progetto.")

        # parte 1
        div1 = DivButtons("La sintesi del progetto")
        div1.add_parag("La presentazione del progetto parte con una esposizione sintetica della nuova iniziativa.")
        div1.add_list("In questa parte indichiamo:* i soggetti che sviluppano l'iniziativa (Sara, Marco, Adriana),# le motivazioni della scelta (La passione per il cake design),# la forma giuridica dell'impresa (Snc),# la mission e la vision (Preparare i migliori dolci del Cilento per gli amanti della qualità della vita - Rendere felici le persone nelle occasioni di incontro),# il prodotto (dolci realizzati con cura artigianale),# il mercato (produzione dolciaria della zona),# la localizzazione (Vallo della lucania),# l'organizzazione (3 soci e un dipendente).")

        # parte 2
        div2 = DivButtons("Esposizione del progetto imprenditoriale e marketing plan")
        div2.add_parag("Il progetto, in questa seconda parte descrittiva, viene descritto in maniera analitica.")
        div2.add_list("Vengono evidenziati:* i motivi di validità del progetto,# i fattori critici di successo,# i tempi di realizzazione,# gli obiettivi e le strategie per raggiungerli.")
        div2.add_parag("Il Marketing plan è parte integrante del business plan.")
        div2.add_list("Esso comprende:* lo studio della situazione di partenza con l'analisi SWOT,# lo studio della domanda dei consumatori (suddivisi in segmenti),# lo studio dei mercati dei fattori produttivi,# lo studio della concorrenza,# il posizionamento dell'impresa,# le strategie di marketing,# il scelte operative di marketing mix,# le modalità di commercializzazione del prodotto.")
        div2.add_parag("A posteriori, le scelte effettuate nel piano di marketing vanno verificate, analizzando gli eventuali scostamenti rispetto a quanto programmato.")


Book()
print_at_console()
create_html_file()
