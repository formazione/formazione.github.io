Operazioni non soggette a IVA: sono quelle che non hanno uno o più presupposti IVA e quelle estranee per legge al campo di applicazione IVA


### Marketing24.html

    File con QARM test (vedi cartella kahoot and glitch per programmi per creare le domande)
    Ho tolto il riferimento alla terza dei file
      ezquiz.js
      easytimer.js
      javascript.min.js


### File da esempio

    lettura_marketing_plan.html



### File con documenti per la scuola con esercizi recenti 11.2.2019

    Ultimamente salvo direttamente nelle cartelle con il nome dell'argomento
    e basta

    H:/azienda_e_gestione
    H:/marketing
    H:/marketing (2019)
    h:/situazione patrimoniale

File per kahoot e Glitch
==============================

    in glitch/testarispostamultipla/
    ci sono i file python per creare da file di testo il codice
    da inserire nei file html per glitch
    e nei file xlsx per kahoot,
    ma, per ora, hanno modi diversi di interpretare 
    le domande con meno di 4 risposte
    glitch sostituisce #
    kahoot, invece, capisce quando finiscono prima,
    per questo ci vogliono ancora due file di testo diversi, per ora.
    PS: sono stati resi compatibili nell'ultima versione.



### Dove inserire un epub creato con Google documenti 11.2.2019

    1. salva un file con google documenti
    2. esportalo come epub
    3. carica il file in https://formazione.github.io/bib/bookshelf
    4. usa questo indirizzo per aprire l'ebook on line
          https://formazione.github.io/bib/i/?book=Marketing.epub


### Testo scorrevole con messaggi nella Home page 11.2.2019

    <!-- the canvas and scrolling text go together -->
    <canvas id="myCanvas"></canvas>
    <script src="https://quinta.glitch.me/scrollingtext.js"></script>
    <!-- the canvas and scrolling text go together -->

### Realizzato da G.G. 2018-2019

### 3bs - 23.01.2019

    h:\situazione patrimoniale

### 4bs 23.01.019

    https://economia2.glitch.me/4bs_es_sp2.html


22/01/2019

    button with javascript, example of function
    
    function textNButton(num, testoparlato, titolo){
      // mostra il testo seguito da un pulsante per legggerlo
      let risposta = testoparlato.split("?")[1];
      let domanda = testoparlato.split("?")[0] + "?";

      // 1. Create the button ============================= BUTTON
      var button = document.createElement("button");
      button.innerHTML = domanda; // the value of the button
      // 2. Append somewhere
      var body = document.getElementsByTagName("body")[0];
      body.appendChild(button);

      // 3. Add event handler
      button.addEventListener ("click", function() {
        speak(risposta);
        button.innerHTML = domanda + "<br><span style='font-size:16px; color:gold'>" + risposta + "</span>";
      });
    }

21/1/2019

    Create tre pagine per ogni classe; index3bs.html ...
    codice per speak

    function speak(cosadire){
     const message = new SpeechSynthesisUtterance(cosadire); 
     window.speechSynthesis.speak(message);
    }
    
    creato marketing.html con lettura testo


20/1/2019

    creato il file 4bs_es_sp1.html da verifiche.html
    sostituita l'immagine della traccia con testo vero e proprio

19/01/2019

    <style>
    @import "temp1.css"
    </style>

15/01/2019
    aggiunti i file 3bs_azienda1
      domande aperte, a risposta multipla...

14/01/2019

    finite 3 domande per la 4a b sala sui ratei
        - 4bs_oa_bilancio1.html
        - 4bs_oa_bilancio2.html
        - 4bs_oa_bilancio3.html
        - 4bs_oa_bilancio4.html
        ...
              * oa sta per one answer 
              (una risposta sola per esercizio)
        
        altri file
        
        - 4bsbilanciomenu.js   contiene il codice comune
          e l'indice
        - temp1.css
        
        Per creare i tre esercizi ho usato:
        H:\javascript_interactive_tests\4bs_bilancio\crea_ratei_passivi.py
        nella cartella versione 2 ho messo questa versione
        dei tre esercizi di oggi


12/1/2019
  
    - 3bs:
    
    - Sabato è stato fatto un cenno allo Stato Patrimoniale
    Soggetti esterni
    Forme giuridiche dell'impresa:
      impresa individuale
      contratto di società
      società di persone

-
    
    4bs:
  
    Esercizio sui ratei e i risconti

-

    5bs: 
  
    Compito, tra venerdì (7 l'hanno fatto) e martedì 15.
    I compiti sono già stati fatti.

11/01/2019

    Esercitazioni
    ==============
    5bs_es1.html
    3bs_es2.html

      


    