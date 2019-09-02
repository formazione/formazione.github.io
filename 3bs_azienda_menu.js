    //         -    C O N F I G U R A T I O N     -
var config = { apiKey: "AIzaSyDp-mWaWEI07pIdRUhi6vA-salEMRWz4hw", authDomain: "quiz-e5e5a.firebaseapp.com", databaseURL: "https://quiz-e5e5a.firebaseio.com/", projectId: "quiz-e5e5a", storageBucket: "quiz-e5e5a.appspot.com", messagingSenderId: "901845403492" }; 
      //  -   I  N I T I A L I Z A T I O N     -
firebase.initializeApp(config);
var database = firebase.database();
function add_data(d,c){ref.child(d).set(c)}

function intro(pref){
  before_domanda.innerHTML += "<center><blockquote>" + pref + "</blockquote></center>";
}

// ============  GO BACK HOME =========
document.write("<a href=\"index.html\"><img src=\"http://icons.iconarchive.com/icons/graphicloads/100-flat/256/home-icon.png\" width=\"100\" />HOME</a>");




function button(es){
  // inserisci il prefisso con il nome assegnato alle pagine + num. pagina
  // es 3bs_sp + es dove 3bs_sp è la parte iniziale del nome del file
  let address = "3bs_azienda" + es + ".html";
    if (document.title[document.title["length"]-1] != es){
    document.write("<button class='btn2' onclick='location.href=\"" + address + "\"'>" + es + "</button>");
    }
}
document.write("<center>");
let img = [];
img[0] = "https://i2.wp.com/news.biancolavoro.it/wp-content/uploads/2017/06/interessi-moratori.jpg?fit=770%2C525&ssl=1"; 

let imgcnt = 0;
button("1", img[imgcnt]);
button("2", img[imgcnt]);
button("3", img[imgcnt]);
button("4", img[imgcnt]);
button("5", img[imgcnt]);
button("6", img[imgcnt]);

document.write("</center>");


document.write("<h4>" + document.title + "</h4>");

let classe = ['-', 'Andreioli', 'Barbato', 'Cirillo', 'Croce', 'DelPiero', 'DiLorenzo', 'DiSevo', 'Giudice', 'Manzo', 'Montemurro', 'NeseLuigi', 'Orlando', 'RibecaLucia', 'Spera', 'ValerioAntonio', 'ValerioFrancesco', 'Verrelli', 'Villano', 'ViteraleFrancesca'] 
    // funzione per creare le opzioni per la scelta del nome dello studente
  // ===================================================================
document.write("<div id='before_domanda'></div>");
function selectStudent(){
  // domanda_top.innerText=compito[data.options[data.selectedIndex].value];
  document.write("<div id=\"domanda_top\"><hr>Istruzioni:<hr>");
  document.write("Seleziona il tuo nome e premi invia per salvare la risposta.<hr><center><b style='color:orange;'>");
  document.write("Teoria</b></center><hr></div>");
  document.write("Seleziona il tuo nome: <select onchange='contenuto.value=compito[data.options[data.selectedIndex].value];button_invio.innerHTML=\"Clicca per inviare la risposta\";' id='data'>");
  for(let i=0; i<classe.length; i++) {
     document.write("<option  value=" + classe[i] + ">" + classe[i] + "</option>");}
  document.write("</select><br>");    
  document.write("Rispondi qui:<br> <textarea id=\"contenuto\" cols=\"80\" rows=\"10\"/> </textarea><br>");
  document.write("<button id=\"button_invio\" onclick=\"add_data(data.value,contenuto.value);this.innerHTML='ok';\"></button>");
}
selectStudent();


// final part
document.write("<hr>")
for (let a in classe){
        document.write("<b style='color:orange'>" + classe[a] + "</b><hr>");
        document.write("<div id='al" + a + "' cols='50' rows='6' value=" + classe[a] + "></div><hr>");
}

// ====================================== PART WITH STUDENTS RESULTS
// Il nome del record viene creato con document.title della pagina che chiama
// questo script...
let ref = database.ref().child(document.title);
let cl_cnt = 0;

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