htmlpage = """<head>
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta http-equiv="content-type" content="text/html; charset=utf-8">
  <meta name="viewport" content="initial-scale=1.0">
    <title>Quiz</title>
    <!-- jquery for maximum compatibility -->
  <link type="text/css" rel="stylesheet" href="https://stackpath.bootstrapcdn.com/twitter-bootstrap/2.2.1/css/bootstrap-combined.min.css">
    <!--<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>-->
  <script src="https://code.jquery.com/jquery-1.11.1.min.js" integrity="sha256-VAvG3sHdS5LqTT+5A/aeq/bZGa/Uj04xKxY8KM/w9EE=" crossorigin="anonymous"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>



<b id="scoretot"></b><br>
<script>

listanomi = [
    "Scegli_il_cognome",
        "Acanfora",
        "Della_Torre",
        "Graniti",
        "Guariglia",
        "Marino",
        "Materazzi",
        "Matrella",
        "Niglio",
        "Orlando",
        "Serra_Davide",
        "Serra_Giulia",
        "Sessa",
            ];

nomi = [
    "Scegli_nome",
        "Sara",
        "Pietro",
        "Andrea",
        "Carmen",
        "Ilaria",
        "Federica",
        "Luca",
        "Federica",
        "Anthony",
        "Alessandro",
        "Federica",
        "Dante",
        "Samuele",
        "Maria Teresa",
        "Roberto",
        "Francesco",
        "Antonio",
        "Francesco",
        "Dennis"
  ];


function select(lista, idsel){
  // l'errore era nel fatto che non avevo messo " + idsel + ", ma solo idsel
  // inoltre devo togliere alla riga 469 la variabile codice che non uso più
  let html = "<select id=" + idsel + " name='carlist' form='carform'>";
  for (nome of lista){
    html +="<option value='"+nome+"'>"+nome+"</option>";
  }
  html += "</select>";
  document.write(html);
}

select(listanomi, 'nomestudente')




</script>



<script src="https://www.gstatic.com/firebasejs/5.9.2/firebase-app.js"></script>
<script src="https://www.gstatic.com/firebasejs/5.9.2/firebase-database.js"></script>
<!-- configurazione  -->
<script src="config.js"></script>
<script>
// nome del record del database 

function start(recordname){
  // crea il record - ricorda di cambiare il record per 
  // esercizi diversi
  ref = database.ref(recordname);
  ref.child("Scegli_il_cognome").set(0)
  ref.on("value", gotData);
  div_scoretot()
}

function div_scoretot(){
  let scoretot = document.getElementById("scoretot");
  scoretot.align = "center";
}

function gotData(data){
  // prende i valori e li scrive in scoretot
    x = data.val();
    for (name in x){
      scoretot.innerHTML += "(" + name + ":" + x[name] + ") ";
  }
}

start("3ce2020_1")


// code = {
//    "Scegli il nome": "",
//         "Maiuri": "Sara",
//         "Saja_P": "Pietro",
//         "Saja_A": "Andrea",
//         "Tierno": "Carmen",
//         "Battagliese": "Ilaria",
//         "Borrelli": "Federica",
//         "Romano": "Luca",
//         "Ciardi": "Federica",
//         "Mautone": "Anthony",
//         "Palladino": "Alessandro",
//         "Ciardi": "Federica",
//         "Carracino": "Dante",
//         "Liguori": "Samuele",
//         "Ricci": "Maria Teresa",
//         "Ghiunghius": "Roberto",
//         "Donnianni": "Francesco",
//         "Merola":"Antonio",
//         "Maiese": "Francesco",
//         "Fluri": "Dennis"
//   };



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
"""