import os

def it_was_in_start():
  """
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
  """



def start(title, imgurl):
  start = """

        <script src="https://unpkg.com/scrollreveal/dist/scrollreveal.min.js"></script>
    <body>"""
  return start


end = """<!-- Bootstrap JS V4 and JQuery V3.3.1 --> <script src="https://code.jquery.com/jquery-3.1.1.slim.min.js" integrity="sha384-A7FZj7v+d/sdmMqp/nOQwliLvUsJfDHW+k9Omg/a/EheAdgtzNs3hpfag6Ed950n" crossorigin="anonymous"></script> <script src="https://cdnjs.cloudflare.com/ajax/libs/tether/1.4.0/js/tether.min.js" integrity="sha384-DztdAPBWPRXSA/3eYEEUWrWCy7G5KFbe8fFjk5JAIxUYHKkDx6Qin1DkWx51bBrb" crossorigin="anonymous"></script> <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/js/bootstrap.min.js" integrity="sha384-vBWWzlZJ8ea9aCX4pEW3rVHjgjt7zpkNpZk+02D9phzyeVkE+jo0ieGizqPLForn" crossorigin="anonymous"></script> <script> window.sr = ScrollReveal(); sr.reveal('.btn', {duration: 2000, origin: 'top', distance: '60px', }); sr.reveal('#bio', {duration: 2000, origin: 'bottom', distance: '100px', reset: true }); sr.reveal('#testimonial', {duration: 2000, origin: 'bottom', viewFactor: 0.3, delay: 1000, reset: true }); sr.reveal('#elsalvador', {duration: 2000, origin: 'bottom', viewFactor: 0.5, reset: true }); sr.reveal('#therose', {duration: 2000, origin: 'bottom', viewFactor: 0.3, reset: true }); sr.reveal('#thecouple', {duration: 2000, origin: 'bottom', viewFactor: 0.3, reset: true }); sr.reveal('#pao', {duration: 2000, origin: 'right', distance: "100px", viewFactor: 0.2, reset: true }); </script> </body> </html>"""


class Header:
  def __init__(self, title, subtitle, urlimg=""):
    global stringa
    self.title = title
    self.subtitle = subtitle
    self.urlimg = urlimg
    stringa += self.slide()

  def slide(self):
    self._slide = """<header class="text-center"> <div> <div class="title"> <h2>""" + self.title + """</h2> <br> <h6>""" + self.subtitle + """</h6> </div> </div> <a href="#bio" class="btn btn-circle"> <i class="fa fa-angle-double-down"></i> </a> </header>"""
    return self._slide

  def print(self):
    print(self.slide())


class TitleAndText(Header):
  def slide(self):
    self._slide = """<!-- BIO --> <section id="bio"> <div class="container"> <div class="row"> <div class="col-12 col-lg-12"> <h2> """ + self.title + """</h2><hr> </div> </div> <!-- First Row end --> <div class="row"> <div class="col-lg-2"></div> <div class="col-12 col-lg-8 text-justify"><p> """ + self.subtitle + """</p> </div> <div class="col-lg-2"></div> </div> <!-- Second Row end --> </div> <!-- Container end--> </section>"""
    return self._slide


class Testimonial(Header):
  def slide(self):
    self._slide = """<section id="testimonial">
    <div class="container">
        <div class="row">
            <div class="col-12 col-lg-12">
                <div class="row text-center">
                  <div class="col-lg-1"></div>
                    <div class="testimonial-left col-4 col-lg-4">
                        <img src=""" + self.urlimg + """ id="consuelo" class="rounded-circle">
                    </div> <!-- Testimonial left end-->
                    <div class="testimonial-right col-8 col-lg-5">
                        <span><i class="fa fa-quote-left"></i> &emsp;""" + self.title + """&emsp; <i class="fa fa-quote-right"></i></span> <br>
                               <footer class="blockquote-footer"> <cite> """ + self.subtitle + """</cite>
                               </footer>
                    </div> <!-- Testimonial right end-->
                    <div class="col-lg-2"></div>
                </div> <!-- Nested Row end -->
            </div> <!-- Col 12 end -->
        </div> <!-- Primary Row end-->
    </div> <!-- Container end -->
</section>"""
    return self._slide


class Classic(Header):

  def slide(self):
    self._slide = """        <!-- CLASSIC SLIDE - TITLE + TEXT + IMG -->
        <section id="elsalvador">
            <div class="container">
                <div class="row">
                    <div class="col-12 col-lg-12">
                      <h2>""" + self.title + """</h2> <hr>
                    </div>
                </div> <!-- First Row end -->
                """
    # This make the subtitle optional... if you just use "" as second argument
    if self._slide != "":
      self._slide += """<div class="row">
                          <div class="col-12 col-lg-8 text-justify">
                              <p>""" + self.subtitle + """</p></div>
                </div> <!-- Second Row end -->"""
    if self.urlimg != "":
      print("non ci sono immagini")
      self._slide += """
                  <div class="row">
                        <div class="col-12 col-lg-8">
                          <img id="lpvolcano" src=""" + self.urlimg + """>
                      </div>
                      <div class="col-lg-2"></div>
                  </div> <!-- Third Row end -->"""

    self._slide += """</div> <!-- Container end -->
        </section>"""

    return self._slide


class TheCouple(Header):
  def slide(self):
    "qui bisogna inserire il titolo, una lista con due stringhe per subtitle e il link ad un video"
    self._slide = """<!-- THE COUPLE -->
<section id="thecouple">
    <div class="container">
        <div class="row">
            <div class="col-12 col-lg-12">
                <div class="row">
                    <div class="col-12 col-lg-12">
                        <h2>""" + self.title + """</h2> <hr>
                    </div>
                </div> <!-- First Nested Row end-->
                <div class="row text-justify">
                    <div class="col-lg-2"></div>
                    <div class="col-12 col-lg-8">
                    <p>""" + self.subtitle[0] + """</p>
                    </div>
                    <div class="col-lg-2"></div>
                </div> <!-- Second Nested Row end -->
                <div class="row">
                    <div class="col-lg-2"></div>
                    <div class="col-8 col-lg-5 text-justify">
                    <p>""" + self.subtitle[1] + """</p>
                    </div>
                    <div class="col-lg-2"></div>
                </div> <!-- Third Nested Row end-->
                <div class="row">
                    <div class="col-lg-2"></div>
                    <div class="col-12 col-lg-8">
                    """ + self.urlimg + """
                    </div>
                    <div class="col-lg-2"></div>
                </div> <!-- Fourth Row end -->
            </div> <!-- Col 12 end -->
        </div> <!-- Primary Row end -->
    </div> <!-- Container end -->
</section>"""
    return self._slide


def video(title, p1, p2, video):
  TheCouple(title, [p1, p2], video)


class Quote(Header):
  def slide(self):
    self._slide = """<style>

    </style>
    <section id="elsalvador">
    <div class="container">
    <div class="row">
                    <div class="col-12 col-lg-12">
    <blockquote class="quote-box">
      <div class="blog-post-actions">
        <p class="blog-post-bottom pull-left">
          """ + self.title + """
        </p>
        <p class="blog-post-bottom pull-right">
          <span class="badge quote-badge">
        </p>
      </div>
      <hr>
      <p class="quote-text">
        """ + self.subtitle + """
      </p>
    </blockquote>
</div></div></div></section>"""
    return self._slide


def music(header, title, filemp3):
  "Shows an mp3 player with a song"
  Classic(header,
          """
    Choose your music:
    <br>
    """ + title + """<br>
    <audio controls>
    <source src=\"""" + filemp3 + """\" type="audio/mpeg">
  </audio>
  """)


class Pdf(Quote):
  def slide(self):
    self.subtitle = """<embed src=\"""" + self.subtitle + """\" width="100%" height="500" type='application/pdf'>"""
    self._slide = """
    <section id="elsalvador">
    <div class="container">
    <div class="row">
                    <div class="col-12 col-lg-12">
    <blockquote class="quote-box">
      <div class="blog-post-actions">
        <p class="blog-post-bottom pull-left">
          """ + self.title + """
        </p>
        <p class="blog-post-bottom pull-right">
          <span class="badge quote-badge">
        </p>
      </div>
      <hr>
      <p class="quote-text">
        """ + self.subtitle + """
      </p>
    </blockquote>
</div></div></div></section>"""
    return self._slide


class Html(Quote):
  def slide(self):
    self.subtitle = """<iframe src=\"""" + self.subtitle + """\" width="100%" height="700"></iframe>"""
    self._slide = """
    <section id="elsalvador">
    <div class="container">
    <div class="row">
                    <div class="col-12 col-lg-12">
    <blockquote class="quote-box">
      <div class="blog-post-actions">
        <p class="blog-post-bottom pull-left">
          """ + self.title + """
        </p>
        <p class="blog-post-bottom pull-right">
          <span class="badge quote-badge">
        </p>
      </div>
      <hr>
      <p class="quote-text">
        """ + self.subtitle + """
      </p>
    </blockquote>
</div></div></div></section>"""
    return self._slide


class Quiz(Header):
  def slide(self):
    self._slide = """<section id="elsalvador">
    <div class = "container">Rispondi alla seguente domanda:</div>
    <div class = "container"><center><h2>""" + self.title + """</h2></center></div>
        <div class="container">
            <div class="row">
                <div class="col-12 col-lg-12">
                    <ul class="pager">
                        <li><a href=javascript:check(""" + self.subtitle.split("/")[0].split(",")[0] + """)>""" + self.subtitle.split("/")[1].split(",")[0] + """</a></li>
                        <li><a href=javascript:check(""" + self.subtitle.split("/")[0].split(",")[1] + """)>""" + self.subtitle.split("/")[1].split(",")[1] + """</a></li>
                        <li><a href=javascript:check(""" + self.subtitle.split("/")[0].split(",")[2] + """)>""" + self.subtitle.split("/")[1].split(",")[2] + """</a></li>
                    </ul>
                </div>
                    <div class="container" id="answer" align="center">?</div>
            </div>
        </div>
    </div>
</section>
    <script>
      function check(ans){
        if (ans == 1){
          answer.style.color = "blue";
        answer.innerHTML = "ESATTO";
          }
        else if (ans==0){answer.innerHTML = "sbagliato";answer.style.color = "red";}
        else if (ans==-1){answer.innerHTML ="errore";answer.style.color = "red";}
      }

      </script>"""
    return self._slide


class Legenda(Header):
  def slide(self):
    if self.title != "":
      addtitle = """<div class = "container"><center><h2>""" + self.title + """</h2></center></div>"""
    else:
      addtitle = ""
    self._slide = """<section id="elsalvador">""" + addtitle + """
        <div class="container">
            <div class="row">
                <div class="col-12 col-lg-12">
                    <ul class="pager">
                        <li><a href=javascript:check(\"""" + self.subtitle.split("/")[0].split(";")[0] + """\")>""" + self.subtitle.split("/")[1].split(";")[0] + """</a></li>
                        <li><a href=javascript:check(\"""" + self.subtitle.split("/")[0].split(";")[1] + """\")>""" + self.subtitle.split("/")[1].split(";")[1] + """</a></li>
                        <li><a href=javascript:check(\"""" + self.subtitle.split("/")[0].split(";")[2] + """\")>""" + self.subtitle.split("/")[1].split(";")[2] + """</a></li>
                    </ul>
                </div>
                    <div class="container" id="answer" align="center">Clicca sui pulsanti per approfondire</div>
            </div>
        </div>
    </div>
</section>
    <script>
      function check(ans){
        answer.innerHTML = ans;
      }

      </script>"""
    return self._slide


def printPageContent():
  "watch the html page generated on the console"
  for s in Header.content:
    print(s)


def header(title, paragraph):
  Header(title, paragraph)


def rejoin(mystring):
  return "%20".join(mystring.split(" "))


# Inizializziamo la funzione che stampa la parte iniziale del file html
title = "Il budget"
urlimg = "https://cdn.allwallpaper.in/wallpapers/1920x1200/10299/japan-tokyo-cityscapes-city-night-1920x1200-wallpaper.jpg"
stringa = start(title, urlimg)


a1 = Classic("A cosa serve il business plan",
             "Prima di iniziare l'attività, l'impresa deve compiere una approfondita serie di analisi dell'ambiente esterno e della situazione aziendale per poter stabilire, dall'inizio, se sussistono le possibilità di successo per la propria idea imprenditoriale. Essa, infatti, non può prescindere dall'analisi dell'offerta e della domanda. Una volta analizzata la situazione esterna ed interna, l'impresa può definire degli obiettivi e delle strategie per raggiungerli, definendoli nei piani aziendali. Il documento che descrivere e sintetizza le informazioni dedotte dalle analisi ambientali e aziendali si chiama business plan. Il business plan contiene l'esposizione delle principali informazioni riguardandi un progetto imprenditoriale necessarie per convincere i finanziatori a finanziare il progetto. Oltre a questa funzione, il business plan è di grande aiuto per il management per prevedere e poi verificare la fattibilità del progetto.")

Classic("Quali sono le parti che lo compongono?",
        "")


Legenda("",
        rejoin("sintesi del progetto con gli elementi esseziali;Descrizione dettagliata del progetto;Analisi dell'aspetto economico, finanziario e patrimoniale") + """/Sintesi del progetto;Esposizione del progetto;Valutazione""")


Classic("La sintesi o executive summary", "Illustra brevemente chi sono i soggetti che vogliono realizzare il progetto, i prodotti o servizi che si vogliono realizzare, i clienti che si intende servire, i mercati, i concorrenti, i mercati di approvvigionamento, l'organizzazione, la vision e la mission.")

Classic("Facciamo un esempio", "Quattro amici vogliono aprire un'attività, un piccolo ristorante nella piazza principale del loro paese. Il paese ha 15.000 abitanti, ma, essendo una località balneare famosa del Sud, d'estate si popola di turisti. I quattro amici si sono conosciuti lavorando in vari ristoranti della zona e del Nord e hanno deciso di mettersi in proprio, forti delle esperienze acquisite negli anni nel settore e trascinati dall'entusiasmo di realizzare il loro comune sogno di poter aprire insieme un'attività ristorativa. Tutti e quattro competenze diverse. Uno di loro è un cuoco, un altro ha fatto il cameriere in molti ristoranti di grande prestigio, un altro ha lavorato come receptionist e l'ultimo ha avuto mansioni direttive in un ristorante per diversi anni. Tutti e quattro lavoreranno a tempo pieno nel ristorante e assumeranno altre due persone in cucina e una in sala. Uno dei soci possiede un locale nella piazza principale da ristrutturare per trasformarlo in ristorante. Gli è stata approvata la domanda per ottenere una misura agevolativa a favore dei giovani imprenditori del Sud. Dato il rapporto di reciproca fiducia, decidono, come forma giuridica, di costituire una società in nome collettivo, i cui tutti sono responsabili illimitatamente per le obbligazioni sociali. Questo tipo di società ha meno obblighi amministrativi rispetto ad una società di capitali.")


Classic("L'esposizione del progetto", "Espone la descrizione dettagliata del progetto, mettendo in luce fattori critici di successo, tempi, obietivi, straegie e il marketing plan. Questo contiene l'analisi SWOT, lo studio della domanda divisa in segmenti, dei mercati di acquisizione, della concorrenza, il posizionamento, le strategie di marketing e il marketing mix.")

Classic("La valutazione del progetto imprenditoriale", "In questa parte vengono presentati i prospetti del piano degli investimenti, il piano finanziario e il bilancio di previsione.")




tabinv2 = """<table border=1 cellspacing=0><tbody><tr>
<td>Immobilizzazione<td colspan=3>costo storico<td>coeff.<td colspan=3>quote annue<tr>
<td><td>n1<td>n2<td>n3<td><td>n1<td>n2<td>n3<tr>
<td>Costi di start up<td> 60 000,00   <td>0<td>0<td>20%<td> 12 000,00   <td> 12 000,00   <td> 12 000,00<tr>
<td>Fabbricato<td> 60 000,00   <td>0<td>0<td>2%<td> 1 200,00   <td> 1 200,00   <td> 12 000,00<tr>
<td>Impianti<td> 180 000,00   <td>0<td>0<td>10%<td> 18 000,00   <td> 18 000,00   <td> 12 000,00<tr>
<td>Arredamento<td> 110 000,00   <td>0<td> 130 000,00   <td>13%<td> 13 750,00   <td> 13 750,00   <td> 30 000,00<tr>
<td>Attrezzature<td> 130 000,00   <td>0<td>0<td>10%<td> 13 000,00   <td> 13 000,00   <td> 13 000,00<tr>
<td>Automezzo<td> 100 000,00   <td>0<td>0<td>20%<td> 20 000,00   <td> 20 000,00   <td> 20 000,00<tr>
<td>Computer<td> 130 000,00   <td>0<td>0<td>20%<td> 26 000,00   <td> 26 000,00   <td> 26 000,00<tr>
<td>Piatti e posate<td>0<td>0<td> 40 000,00   <td>15%<td>0<td>0<td> 6 000,00<tr>
<td>Tovagliato<td>0<td>0<td> 170 000,00   <td>25%<td>0<td>0<td> 42 500,00
<tbody></table>"""

a1 = Classic("Piano degli investimenti", tabinv2)
Classic("", "In questo prospetto vediamo quali siano gli investimenti progettati per i prossimi tre anni. A parte gli investimenti iniziali, si prevede di fare nuovi investimenti nel terzo anno, come si può osservare nella tabella precedente.")

"""
Classic("La sintesi o executive summary")

Classic("L'espozione del progetto")

Classic("I marketing plan")

Classic("La valutazione del progetto")
"""

# video("Budget delle vendite", "Vediamo come si calcolano i ricavi nel budget delle vendite", "",
#      """<iframe width="100%" height="480" src="https://www.youtube.com/embed/9m1YOQMlJek" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>""")

# ==============  {  FINE DELLA PRESENTAZIONE } =====================  #


# Address of the image of the header

stringa += end


with open('busplan.html', 'w', encoding='utf-8') as file:
  file.write(stringa)

os.system("busplan.html")
