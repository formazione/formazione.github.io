let prefissopagine = "5bs_marketing"; // vai a button(es)

let domanda = []; // conterrà tutte le domande
let risposte = []; // ... le risposte
let compito = {}; // assegna ad ogni alunno la domanda

function add_data(d,c){
  // richiamato quanto di clicca il pulsante della risposta dopo la textarea
  var database = firebase.database();
  let ref = database.ref(document.title);
  ref.child(d).set(c)
}

function tastohome(){
  // tasto home
var divElement = document.createElement("Div");
divElement.id = "divID";
divElement.style.position = "fixed";
divElement.style.top = "40px";
divElement.style.left = "20px";
divElement.style.textAlign = "center";
divElement.style.fontWeight = "bold";
divElement.style.fontSize = "smaller";
divElement.style.paddingTop = "15px";
var img = document.createElement("img");
img.src = "https://lensofliberty.org/wp-content/uploads/2016/08/home-icon.ico";
img.width = "100";
var a = document.createElement('a');
var linkText = document.createTextNode("Home");
a.appendChild(img);
a.title = "my title text";
a.href = "index_esercizi.html";
divElement.appendChild(a);
document.getElementsByTagName("body")[0].appendChild(divElement);
}
  
function introduzione(){
  // Intestazione e immagine : argomento, imgaddress e spiegazione sono personalizzabili nei file
  document.write("<div id=\"domanda_top\"><hr>" + argomento + "<hr>");
  domanda_top.innerHTML += "<blockquote>";
  domanda_top.innerHTML += spiegazione;
  domanda_top.innerHTML += "</blockquote>";
  // IMGADDRESS viene definito nelle singole pagine - è personalizzabile
  domanda_top.innerHTML += "<center><img src=\'" + imgaddress +"\' width=25% /></center>";
}

function crealistadomande(){
  // =========== CODICE CHE ELABORA creadomanda() nei file HTML ======
  //quanto testo è uguale a qualcosa la domanda è la stessa per tutti
  // quando è uguale a "", si aggiunge una domanda diversa per ognuno
  // con domanda[0] = "..."; Per la 3bs le domande vanno da 0 a 19
  for (let n=0; n<20; n++){
    // Questo codice è per le domande tutte uguali
    if (creadomanda()[0] != ""){
      let alunno = classe[n] + ":"
      let text = creadomanda()[0]; // è nel file dell'esercizio
      console.log(text);
      let correttore = creadomanda()[1]; // dal file dell'esercizio
      domanda.push(text);
      risposte.push(correttore);
    }
    // Se testo è uguale a "" si aggiungono le domande singole con domanda[0] = "..."
    else {}
  }
}

function assegnadomande(){
    let cnt = 0
        for (n in classe){
         compito[classe[n]] = domanda[n]; // se la domanda è uguale non serve ++
    }
}
 

function vedisoluzioni(){
  for (i in domanda) console.log(domanda[i]);
  for (i in domanda) console.log(domanda[i] + risposte[i]);

}


function button(es){
    // inserisci il prefisso con il nome assegnato alle pagine + num. pagina
    // es 3bs_sp + es dove 3bs_sp è la parte iniziale del nome del file
    let address = prefissopagine + es + ".html";
      if (document.title[document.title["length"]-1] == es){
      document.write("<button class='btn4' onclick='location.href=\"" + address + "\"'>" + es + "</button>");
      }
    else 
      document.write("<button class='btn2' onclick='location.href=\"" + address + "\"'>" + es + "</button>");
}

function trigger(){
  // quando si sceglie l'alunno...
  spaziodomanda.innerHTML="<pre>" + compito[data.options[data.selectedIndex].value] + "</pre>";
  contenuto.value=compito[data.options[data.selectedIndex].value];
  button_invio.innerHTML = "Clicca per inviare la risposta";
}

function selectStudent(){
  // domanda_top.innerText=compito[data.options[data.selectedIndex].value];
  document.write("Seleziona il tuo nome: <select onfocus='trigger();' onchange='trigger();' id='data'>");
  for(let i=0; i<classe.length; i++) {
     document.write("<option  value=" + classe[i] + ">" + classe[i] + "</option>");}
  document.write("</select><br>");
}

function createtextarea(){
  // crea lo spazio per vedere la domanda e la textarea
  document.write("<div id='spaziodomanda' style='color:coral;font-size:.5em;'></div>");
  document.write("Rispondi qui:<br><textarea id=\"contenuto\" cols=\"80\" rows=\"10\"/> </textarea><br>");
  document.write("<button id=\"button_invio\" onclick=\"add_data(data.value,contenuto.value);this.innerHTML='ok';\"></button>");
}

let ris = "";
function answ(){
  ris = "<b style='color:lime'>[R:] > </b>";
 return ris;
}


function retrieveData(){
  // I finally discovered how to retieve all the data
  var database = firebase.database();
  let ref = database.ref(document.title);
  
  
  let cl_cnt = 0
  ref.child(classe[cl_cnt++]).on("value", snap => al0.innerText = snap.val());
ref.child(classe[cl_cnt++]).on("value", snap => al1.innerText = snap.val());
ref.child(classe[cl_cnt++]).on("value", snap => al2.innerText = snap.val());
ref.child(classe[cl_cnt++]).on("value", snap => al3.innerText = snap.val());
ref.child(classe[cl_cnt++]).on("value", snap => al4.innerText = snap.val());
ref.child(classe[cl_cnt++]).on("value", snap => al5.innerText = snap.val());
ref.child(classe[cl_cnt++]).on("value", snap => al6.innerText = snap.val());
ref.child(classe[cl_cnt++]).on("value", snap => al7.innerText = snap.val());
ref.child(classe[cl_cnt++]).on("value", snap => al8.innerText = snap.val());
ref.child(classe[cl_cnt++]).on("value", snap => al9.innerText = snap.val());
ref.child(classe[cl_cnt++]).on("value", snap => al10.innerText = snap.val());
ref.child(classe[cl_cnt++]).on("value", snap => al11.innerText = snap.val());
ref.child(classe[cl_cnt++]).on("value", snap => al12.innerText = snap.val());
ref.child(classe[cl_cnt++]).on("value", snap => al13.innerText = snap.val());
ref.child(classe[cl_cnt++]).on("value", snap => al14.innerText = snap.val());
ref.child(classe[cl_cnt++]).on("value", snap => al15.innerText = snap.val());
  ref.child(classe[cl_cnt++]).on("value", snap => al16.innerText = snap.val());
  ref.child(classe[cl_cnt++]).on("value", snap => al17.innerText = snap.val());
  ref.child(classe[cl_cnt++]).on("value", snap => al18.innerText = snap.val());
  ref.child(classe[cl_cnt++]).on("value", snap => al19.innerText = snap.val());
  // la 5bs ha 22 alunni, quindi fino ad al21
  ref.child(classe[cl_cnt++]).on("value", snap => al20.innerText = snap.val());
  ref.child(classe[cl_cnt++]).on("value", snap => al21.innerText = snap.val());

  
  
  
}



function configFirebase(){
  var config = { apiKey: "AIzaSyDp-mWaWEI07pIdRUhi6vA-salEMRWz4hw", authDomain: "quiz-e5e5a.firebaseapp.com", databaseURL: "https://quiz-e5e5a.firebaseio.com/", projectId: "quiz-e5e5a", storageBucket: "quiz-e5e5a.appspot.com", messagingSenderId: "901845403492" }; 
  firebase.initializeApp(config);
}

// final part
function printresult(){
  document.write("<hr>")
  for (let a in classe){
          document.write("<b style='color:orange'>" + classe[a] + "</b><pre style='font-size:.5em'>" + compito[classe[a]] + "</pre>");
    // qui è dove va la risposta data nella textarea dopo aver cliccato il pulsante
    // la risposta è memorizzata in firebase
    document.write("<div id='al" + a + "' cols='50' rows='6' value=" + classe[a] + " style='color:cyan; background:darkblue;'></div><hr>");
  }
}

// =============================== INIZIO DELLA PAGINA COMUNE PER TUTTI ===============
document.write("<center>");
//Pulsanti per navigare tra gli esercizi
for (let n=1; n<7; n++){  button(n);}
document.write("</center>");
// titolo
document.write("<h4>" + document.title + "</h4>");

let classe = ['Amatruda Massimo', 'Bortone Tommaso', 'Cantalupo Giuseppe', 'Caputo Nicola', 'Carbone giuseppe', 'Cutrì Roberto', 'Del gaudio Giuseppe', 'Di Santi Angela', 'Krzesinska Paulina', 'Lettieri Stefania', 'Lista Celestino', 'Maiese Giuseppe', 'Maiuri Claudia', 'Merola Giuseppina Pia', 'Moscatiello Anna Rita', 'Ridolfi Erika', 'Ruocco Michele', 'Schiavo Angela', 'Spera Aurelia', 'Tancredi Marika', 'Vaccaro Domenico', 'Vassalluzzo Benedetta']

// =================================== DOPO VIENE START() RICHIAMATA DALLE PAGINE ==========

function start(){
  // la funzione start viene usata nei singoli file html con gli esercizi
  tastohome();
  introduzione();
  selectStudent();
  createtextarea();
  crealistadomande();
  assegnadomande();
  vedisoluzioni();
  printresult();
  configFirebase();
  retrieveData();
}