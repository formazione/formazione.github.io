"""
CREATE HTML QUIZ
FROM A TXT FILE LIKE THIS

Quanto scoppiò la rivoluzione francese?
1789
1790
1800
1801
"""
import tkinter as tk
import os

def create():
    with open("exercise.html", "w", encoding="utf-8") as file:
        file.write(html)

root = tk.Tk()
root.geometry("300x300")
root.title("4 C E")


html = """

<head>
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta http-equiv="content-type" content="text/html; charset=utf-8">
  <meta name="viewport" content="initial-scale=1.0">
    <title>Quiz</title>
    <!-- jquery for maximum compatibility -->
  <link type="text/css" rel="stylesheet" href="https://stackpath.bootstrapcdn.com/twitter-bootstrap/2.2.1/css/bootstrap-combined.min.css">
    <!--<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>-->
  <script src="https://code.jquery.com/jquery-1.11.1.min.js" integrity="sha256-VAvG3sHdS5LqTT+5A/aeq/bZGa/Uj04xKxY8KM/w9EE=" crossorigin="anonymous"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>



<!--       firebase : copia da qui fino alla fine di script  -->

<script src="https://www.gstatic.com/firebasejs/5.9.2/firebase-app.js"></script>
<script src="https://www.gstatic.com/firebasejs/5.9.2/firebase-database.js"></script>
<br>

<!--- questo era per inserire il nome a mano 
Nome: <input id="nomestudente" type="text">
-->

<script>

code = {
      "Maiuri": "000",
      "Battagliese": "000",
      "Borrelli": "000",
      "Carracino": "000",
      "Ciardi": "000",
      "Donnianni": "000",
      "Fluri": "000",
      "Ghiunghius": "000",
      "Liguori": "000",
      "Maiese": "000",
      "Mautone": "000",
      "Merola": "000",
      "Palladino": "000",
      "Ricci": "000",
      "Romano" : "000",
      "Saja_A": "000",
      "Saja_P": "000",
      "Tierno": "000",
  };

// Nome del test che diventa un child di firebase
// the name is taken from the text file name where the questions are
let record_firebase = "4ce_budget";


/* CREA LA LISTA E QUANDO CAMBIA STUDENTE CAMBIA IMMAGINE id=nomstu
trovi il div placeholder della immagine qualche riga sotto
*/

function namePng(name){
  return "../" + name + ".PNG";
}

let html = "<select id='nomestudente' name='carlist' form='carform' onchange='nomstu.src=namePng(nomestudente.value)'>";

listanomi = [];
for (nome in code){
  html +="<option value='"+nome+"'>"+nome+"</option>";
  listanomi.push(nome);
}
html += "</select>";
document.write(html);





// fine dati alunni, ricorda di modificare l'esercizio

</script>

    <!-- -------------------- Casella codice -------------------->
<img id="nomstu" width=50>
<script>
nomstu.src= "../" + nomestudente.value + ".PNG"
  </script>
Codice: <input id="codice" type="text" value=000>


<div class="form-group rsform-block rsform-block-framecontent">
<div id="frame" role="content"></div>
</div>
<b id="scoretot"></b>


<script>
  // Initialize Firebase
  var config = {
    apiKey: "AIzaSyDp-mWaWEI07pIdRUhi6vA-salEMRWz4hw",
    authDomain: "quiz-e5e5a.firebaseapp.com",
    databaseURL: "https://quiz-e5e5a.firebaseio.com",
    projectId: "quiz-e5e5a",
    storageBucket: "quiz-e5e5a.appspot.com",
    messagingSenderId: "901845403492"
  };
  firebase.initializeApp(config);
  let database = firebase.database();


  // Nome del child dove vanno i risultati ====== !!! ====>>>
  let ref = database.ref(record_firebase);
  
  // ref.set(); // usa questo per cancellare tutti i dati delete all

  ref.on("value", gotData)

  let scoretot = document.getElementById("scoretot");
scoretot.align = "center";
function gotData(data){
    x = data.val();
    for (name in x){
  scoretot.innerHTML += "<img src='../" + name + ".PNG' width='100'>(" + name + ":" + x[name] + ") ";
}
}

</script>


<script type="text/javascript">


    var quiztitle = "Pianificazione e programmazione";

    /**
    * Set the information about your questions here. The correct answer string needs to match
    * the correct choice exactly, as it does string matching. (case sensitive)
    *
    */

// ========================== Nuova funzione speak ===========
function speak(x) {
  synth = speechSynthesis
  utt = new SpeechSynthesisUtterance(x);
  synth.speak(utt);
  is_on = 1;
}
      
function shuffle(array) {
  var currentIndex = array.length, temporaryValue, randomIndex;
  while (0 !== currentIndex) {
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;
    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }
  return array;
}
      
if (!("scramble" in Array.prototype)) {
  Object.defineProperty(Array.prototype, "scramble", {
    enumerable: false,
    value: function() {
      var o, i, ln = this.length;
      while (ln--) {
        i = Math.random() * (ln + 1) | 0;
        o = this[ln];
        this[ln] = this[i];
        this[i] = o;
      }
      return this;
    }
  });
}   

//--let mydom =;

      
  // -------- substitute this -----------------    
function createQuiz(){
  // returns a list with data in {} for each question
  let quiz = [];
  mydom = mydom.split("\\n");
  console.log(mydom);
  // mescola le domande
  mydom.sort(function() {return .5 - Math.random();});
  for (d in mydom){
      let darr = mydom[d].split("___");
    domanda = darr[0];
    corretta = darr[1];
    console.log(darr);
      let dnew = darr.reverse();
      dnew.pop();
      dnew.sort(function() {return .5 - Math.random();});
      // ------------- quiz.push ---------------------
      quiz.push({
          "question": domanda,
          "image":  "",
          "choices": dnew,
          "correct": corretta,
          "explanation": ""
        })
      // ---------------------------------------------
  }
  return quiz;
}
      
let quiz = createQuiz(); // returns a list with data in {} for each question
 

      

      
var currentquestion = 0, score = 0, submt=true, picked;
let count_speak = 0;
      
      
jQuery(document).ready(function($){
  
  function addChoices(choices){
      if(typeof choices !== "undefined" && $.type(choices) == "array"){
        $('#choice-block').empty();
        for(var i=0;i<choices.length; i++){
          // added .css({'font-size':'36px'}) il 2 marzo 2019
        $(document
          .createElement('li'))
          .addClass('choice choice-box btn')
          .attr('data-index', i)
          .html(choices[i])
          .appendTo('#choice-block')
          .css({'font-size':'28px'});   //  Aggiunge risposte
      }
    }

  }
                 

  
  
  function nextQuestion(){
     
      submt = true;
      $('#explanation').empty(); // svuota spiegazione
      $('#question').text(quiz[currentquestion]['question']); // domanda attuale
      // domanda n. di ... totale domande
      $('#pager').text('Domanda' + Number(currentquestion + 1) + ' di ' + quiz.length);
      // Immagine... ?
      if(quiz[currentquestion].hasOwnProperty('image') && quiz[currentquestion]['image'] != ""){
        if($('#question-image').length == 0){
          $(document.createElement('img'))
            .addClass('question-image')
            .attr('id', 'question-image')
            .attr('src', quiz[currentquestion]['image'])
            .attr('alt', (quiz[currentquestion]['question']))
            .insertAfter('#question');
        } else {
          $('#question-image')
            .attr('src', quiz[currentquestion]['image'])
            .attr('alt', (quiz[currentquestion]['question']));
        }
      } else {
        $('#question-image')
          .remove();
      }

      addChoices(quiz[currentquestion]['choices']);
      setupButtons();
      // parla solo una volta ======|||||||||=====>>>
      if (count_speak==0 && is_on==1){
        speak(quiz[currentquestion]['question']);
        count_speak = 1;
      }
    // >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  parla solo una volta ======|||||||||=====>>>
    
      jQuery(document).ready(function($){
        $("#question").html(function(){
          var text= $(this).text().trim().split(" ");
          var first = text.shift();
          return (text.length > 0 ? "<span class='number'>"+ first +"</span> " : first) + text.join(" ");
        });
        
        $('p.pager').each(function(){
          var text = $(this).text().split(' ');
          if(text.length < 2)
            return;
          
          text[1] = '<span class="qnumber">'+text[1]+'</span>';
          $(this).html(
            text.join(' ')
          );
        });
      });
        
      
        } // function nextQuestion


function processQuestion(choice){  
    // ===========   Risposta ESATTA!  ============================== //
    if(quiz[currentquestion]['choices'][choice] == quiz[currentquestion]['correct'])
      {
        $('.choice')
          .eq(choice)
          .addClass('btn-success')
          .css({'font-size':'36px', 'font-weight':'bold', 'border-color':'#51a351', 'color':'#fff'});
        $('#explanation')
          .html('<span class="correct">ESATTO!</span> ' + (quiz[currentquestion]['explanation']));
        
        let ff = [
                  "accipicchia che bravura",
                  "bene",
                  "benissimo",
                  "bravo o brava",
                  "bravo",
                  "certo!",
                  "ci siamo",
                  "complimenti per la risposta",
                  "congratulazioni",
                  "continua così",
                  "corretto",
                  "eh sì",
                  "eccezionale",
                  "esatto",
                  "fantastico",
                  "favoloso",
                  "geniale",
                  "giusto",
                  "giusto",
                  "grande",
                  "hai risposto bene",
                  "mamma mia",
                  "meraviglia",
                  "ok",
                  "ottimo",
                  "ottimo risultato",
                  "perfetto",
                  "proprio così",
                  "risposta esatta",
                  "stai andando bene",
                  "sì",
                  "sì, sì",
                  "sìì",
                  "ti stai impegnando",
                  "yes",
                  ].sort(function(){return 0.5 - Math.random()})[0];
        speak(ff);
        score++;
        count_speak = 0;
      } 
      
    // ================================ |  Risposta sbagliata  | ======================== //
    else {
      $('.choice')
            .eq(choice)
            .addClass('btn-danger')
            .css({'font-weight':'bold', 'border-color':'#f93939', 'color':'#fff'});
      $('#explanation')
        .html('<span class="incorrect">INESATTO!</span> ' + (quiz[currentquestion]['explanation']));
        speak("No! è " + quiz[currentquestion]['correct']);
            }
        count_speak = 0;
        currentquestion++;
    // ========================= qui è stata aggiunta da 322
    if (currentquestion < quiz.length)  nextQuestion();
    // =========================
  

      // SONO FINITE LE DOMANDE... MOSTRA I RISULTATI
      if(currentquestion == quiz.length){
        $('#submitbutton')
          .html('GET QUIZ RESULTS')
          .removeClass('btn-success')
          .addClass('btn-info')
          .css({'border-color':'#3a87ad', 'color':'#fff'})
          .on('click', function(){
          
              $(this).text('GET QUIZ RESULTS')
                .on('click');
          endQuiz();
        })
        
      }
      
      else if (currentquestion < quiz.length){ 
      // SE CI SONO ANCORA DOMANDE, RIMETTE IL PULSANTE CONTROLLA LA RISPOSTA
        
        $('#submitbutton').html(' VERIFICA >>> ')
          .removeClass('btn-success')
          .addClass('btn-warning')
          .css({'font-weight':'bold', 'border-color':'#faa732', 'color':'#fff'})
          .off('click', function(){
          
        $(this).text('VERIFICA')
          .removeClass('btn-warning')
          .addClass('btn-success')
          .css({'font-weight':'bold', 'border-color':'#51a351', 'color':'#fff'})
          .on('click');
          
        })
        
      } 
    
    else {
        $('#submitbutton').html('VAI ALLA PROSSIMA DOMANDA &raquo;').on('click', function(){
        $(this).text('- CONTROLLA LA RISPOSTA -').css({'color':'inherit'}).on('click');
        })
      }

          
      
    }

       
                                  /*
                                  
                                  Qui sotto c'è il codice che segue
                                  la scelta di una opzione
                                                |
                                                |
                                               \/
                                  */
  
  
  function setupButtons(){
      $('.choice').on('click', function(){
      //speak(quiz[currentquestion]['choice'])
    // Ogni volta che clicco un pulsante
      
        synth.cancel();
        is_on = 0;
    
            
        picked = $(this).attr('data-index');
        $('.choice').removeAttr('style').off('mouseout mouseover');
        $(this).css({'font-weight':'900', 'border-color':'#51a351', 'color':'#51a351', 'background' : 'gold'});
        if(submt){
          submt=false;
          $('#submitbutton').css({'color':'#fff','cursor':'pointer'}).on('click', function(){
            $('.choice').off('click');
            $(this).off('click');
            processQuestion(picked);
            //
          });
        }
      })
    }
        
        
  
  
  function endQuiz(){
      $('#explanation').empty();
      $('#question').empty();
      $('#choice-block').empty();
      $('#submitbutton').remove();
      $('.rsform-block-submit').addClass('show');
      $('#question').text("Hai risposto bene a " + score + " domande su " + quiz.length + " complessive.");
      speak("hai risposto in modo corretto a " + score + " domande su " + quiz.length + " complessive");

//==================================== ##################### ====
//let nomestu = document.getElementById("nomestudente");
scoretot.innerHTML = "";

let nome = nomestudente.value;
// Vale solo la prima volta
//if (listanomi.includes(nomestudente.value) && code[nomestudente.value]==codice.value && x[nomestudente.value] == undefined){

if (listanomi.includes(nomestudente.value) && code[nomestudente.value]==codice.value){
  ref.child(nome).set(Math.round(score/quiz.length * 100));
}

// ========================================================
      
      let percent = Math.round(score/quiz.length * 100);
      speak(nomestudente.value);
      if (percent == 100) speak("Hai ottenuto il massimo punteggio! Ottimo!");
      else if (percent < 100 && percent >80) speak("Bel risultato, complimenti");
      else if (percent < 80 && percent >70) speak("Hai risposto in modo discreto, bravo.");
      else if (percent < 70 && percent >60) speak("HAi risposto in modo sufficientemente corretto.");
      else speak("Devi impegnarti di più. Riprova");
    
      $(document.createElement('p')).addClass('score').text(nomestudente.value).insertAfter('#question');
      $(document.createElement('p')).addClass('score').text(Math.round(score/quiz.length * 100) + '%').insertAfter('#question');      
    }

        /**
         * Runs the first time and creates all of the elements for the quiz
         */
    function init(){
      speak(quiz[currentquestion]['question'])
      //add title
      /*
      if(typeof quiztitle !== "undefined" && $.type(quiztitle) === "string"){
        $(document.createElement('h2')).text(quiztitle).appendTo('#frame');
      } else {
        $(document.createElement('h2')).text("Quiz").appendTo('#frame');
      }
      I removed the title to leave more space */
      
      //add pager and questions
      if(typeof quiz !== "undefined" && $.type(quiz) === "array"){
        //add pager
        
        $(document.createElement('p')).addClass('pager').attr('id','pager').text('Domanda 1 di ' + quiz.length).appendTo('#frame');
        //add first question
        $(document.createElement('h3')).addClass('question').attr('id', 'question').text(quiz[0]['question']).appendTo('#frame');
        //add image if present
        if(quiz[0].hasOwnProperty('image') && quiz[0]['image'] != ""){
          $(document.createElement('img')).addClass('question-image').attr('width','100px').attr('id', 'question-image').attr('src', quiz[0]['image']).attr('alt', (quiz[0]['question'])).appendTo('#frame');
        }
        
        $(document.createElement('p')).addClass('explanation').attr('id','explanation').html('').appendTo('#question');
        
        //questions holder
        $(document.createElement('ul')).attr('id', 'choice-block').appendTo('#frame');
        
        //add choices
        addChoices(quiz[0]['choices']);
        
        //add submit button
        $(document.createElement('div')).addClass('btn-warning choice-box').attr('id', 'submitbutton').text('VERIFICA >>>').css({'font-weight':'bold', 'color':'#fff','padding':'30px 0', 'border-radius':'10px'}).appendTo('#frame');
        
        setupButtons();
      }
    }
  
    init();
  
  });
    
  jQuery(document).ready(function($){     
    $("#question").html(function(){
    var text= $(this).text().trim().split(" ");
    var first = text.shift();
      return (text.length > 0 ? "<span class='number'>"+ first +"</span> " : first) + text.join(" ");
    });
    
    $('p.pager').each(function(){
      var text = $(this).text().split(' ');
      if(text.length < 2)
        return;
      
      text[1] = '<span class="qnumber">'+text[1]+'</span>';
      $(this).html(
        text.join(' ')
      );
    });

  }); 

    function copyText() {
      var output = document.getElementById("frame").innerHTML;
      document.getElementById("placecontent").value = output;
    }
      
    </script>
    <style type="text/css" media="all">
      
      .btn:hover, .btn:active {
        color: blue;
        font-weight: 800;
      background-image: url("http://www.myiconfinder.com/uploads/iconsets/65192ff2984e9928d32fd577bc743ea5.png");
        background-size: 100%;
  
      }

      /*        BODY                 */
body {
    margin: 0;
    font-family: "Consolas",Helvetica,Arial,sans-serif;
    font-size: 24px;
    line-height: 20px;
    color: #ffffff;
    background-color: #21517ee8;
}
    h3.question {
    font-family: "Consolas",Helvetica,Arial,sans-serif;
    font-weight: normal;
    margin: 20px 0;
    padding: 0;
    font-style: italic;
    display: block;
    color: whitesmoke;
    
}  
      
    input   
      
      { height:30px !important; }
      
    input[type=checkbox]
      
      { height:30px !important; margin-top:-3px !important; 
        margin-right:5px !important; box-shadow:none; background-color:#ffffff;
        position:relative !important; }
      
    textarea                        
      { width: 90%; margin: 0 auto; display: block; }
      
    input[type=radio]               
      { height:30px !important; margin-top:-3px !important; margin-right:5px !important; box-shadow:none; background-color:#ffffff; position:relative !important; }
      
    .form-group input, .form-group select           { height:30px; padding: 0px 12px; }
    .form-horizontal .form-group              { margin:10px; }
    .formContainer .formControlLabel            { width:auto !important; min-width:150px; margin:0; padding:0; }
    .formControls                     { width:100%; padding:0; margin: 10px 0 20px auto; }
    .radio                          { padding-top:0 !important; padding-left:8px !important; }
    .radio-inline                     { margin-right:10px; padding-top:0 !important; display:inline; }
    .bold                         { font-weight:bold; }
    .italic                         { font-style:italic; }
    .clear                          { width:100%; margin:0 !important; }
    .rsform-block-submit                  { display:none; }
    .show                           { display: block !important; }
    #submit                         { margin:0 auto; display:block; }

    /* QUIZ STYLES */
      li.choice-block {font-size: 28px};
    ol,ul                           { list-style:none; font-size: 48}
    strong                          { font-weight:700; }
    #frame                          { width:auto; max-width: 800px; background:transparent; margin:3px auto; padding:10px;     color: #f94a4a !important; }
    div#frame h2 ul li                      { color: white; width:auto; border-bottom:1px solid #bdbdbd; padding:0 0 5px 0; font-size:32px; }
    h3.question                       { font-weight:normal; margin:20px 0; padding:0; font-style:italic; display:block; }
    p.pager                         { margin:5px 0 5px; color:#999; text-align:right; }
    .qnumber                        { font-size:25px; font-weight:bold; font-style:italic; vertical-align:bottom; }
    .number                         { font-family: "Consolas",Helvetica,Arial,sans-serif;font-size:24px; font-weight:bold; font-style:normal; vertical-align:inherit; padding-right:10px; }
    .score                          { width:100%; display:inline-block; margin:30px 0; font-size:100px; text-align:center; }
    img.question-image                    { width:25%; height:auto; display:block; max-width:150px; margin:10px auto; border:1px solid #ccc; }
    #choice-block                       { display:block; list-style:none; margin:0; padding:0; cursor: pointer; }
  /*  #submitbutton                       { cursor:pointer; -webkit-border-radius: 5px; -moz-border-radius: 5px; border-radius: 5px; } */
  /*  #submitbutton:hover                   { background:#7b8da6; } */
    #explanation                      { width:auto; min-height:0px; margin:0 auto; padding:0px 0; text-align:center;}
    #explanation span                     { font-weight:bold; padding-right:8px; }
    .choice-box                       { width:100%;  display:block;  text-align:center;  margin:5px auto !important; padding:10px 0 !important; border:1px solid #bdbdbd; }
      .choice-box.btn {font-size: 28px;}
    .correct                        { color:#51a351; font-size: 32px; display: block; margin-bottom: 5px; border-bottom: 1px #51a351 solid; padding-bottom: 5px; }
    .incorrect                        { color:#f93939; font-size: 32px; display: block; margin-bottom: 5px; border-bottom: 1px #f93939 solid; padding-bottom: 5px; }
    
#body{
width:100vw;
height:100vh;
}
 
    </style>

</head>

  
</script>


<!-- cannot right click 
<body  oncontextmenu="return false">
-->







"""








def check(event):
    global html
    ind = lstb.curselection()[0]
    filename = lstb.get(ind)
    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()
    # print(text)
    text = text.split("\n\n")
    for n,t in enumerate(text):
        text[n] = t.replace("\n","___")
    text = "\n".join(text)
    # print(text)
    text = text.replace("'","\'")
    
    # Added these two lines in _2 version to get the name of the record from the txt file
    # with the questions; change the name of the class for the different classes
    record_name = "4ce_" + lstb.get(ind)[:-5]
    html = html.replace("4ce_budget", record_name)

    html = html.replace("//--let mydom =;", "let mydom = `" + text + "`;")
    filename = "quiz/" + filename[:-5] + ".html"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(html)
    print(filename)
    os.system("start " + filename)
    root.destroy()

lstb = tk.Listbox(root)
lstb.pack()
lstb.bind("<Double-Button>", check)

for file in os.listdir():
  if file.endswith(".quiz"):
    lstb.insert(tk.END, file)


root.mainloop()