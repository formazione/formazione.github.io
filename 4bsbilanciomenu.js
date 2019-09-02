    //         -    C O N F I G U R A T I O N     -
var config = {
  apiKey: "AIzaSyDp-mWaWEI07pIdRUhi6vA-salEMRWz4hw",
  authDomain: "quiz-e5e5a.firebaseapp.com",
  databaseURL: "https://quiz-e5e5a.firebaseio.com/",
  projectId: "quiz-e5e5a",
  storageBucket: "quiz-e5e5a.appspot.com",
  messagingSenderId: "901845403492"
};

      //  -   I  N I T I A L I Z A T I O N     -
firebase.initializeApp(config);
var database = firebase.database()
function add_data(d,c){ref.child(d).set(c)}

function intro(pref){
  before_domanda.innerHTML += "<center><blockquote>" + pref + "</blockquote></center>";
}

// ============================================== menu
document.write("<div id='home'><a href=\"index.html\">[ Home ] </a></div>");

function button(es, address){
  // non visualizza il bottone per la pagina attuale
    if (document.title[document.title["length"]-1] != es){
    document.write("<button class='btn2' onclick='location.href=\"" + address + "\"'>" + es + "</button>");
    }
}
document.write("<center>");
button("1","4bs_oa_bilancio1.html");
button("2","4bs_oa_bilancio2.html");
button("3","4bs_oa_bilancio3.html");
button("4","4bs_oa_bilancio4.html");
button("5","4bs_oa_bilancio5.html");
button("6","4bs_oa_bilancio6.html");
button("7","4bs_oa_bilancio7.html");
button("8","4bs_oa_bilancio8.html");
document.write("</center>");


document.write("<h4>" + document.title + "</h4>");


let classe = [
      "-",
      "Correale",
      "Dapolito",
      "Galietta",
      "Giordano",
      "Guariglia",
      "Landi",
      "Lembo",
      "Mainente",
      "Malzone",
      "Mauro",
      "Mazziotti",
      "Pepe",
      "Puglia",
      "Saturno",
      "Scelza",
      "Tardio"
    ];

    // funzione per creare le opzioni per la scelta del nome dello studente
  // ===================================================================
document.write("<div id='before_domanda'></div>");
function selectStudent(){
  document.write("Seleziona il tuo nome: <select onchange='contenuto.value=compito[data.options[data.selectedIndex].value];button_invio.innerHTML=\"Clicca per inviare la risposta\";' id='data'>");
  for(let i=0; i<classe.length; i++) {
     document.write("<option  value=" + classe[i] + ">" + classe[i] + "</option>");}
  document.write("</select><br>");    
  document.write("Domanda:<div id=\"domanda_top\"></div><br>Rispondi qui:<br> <textarea id=\"contenuto\" cols=\"80\" rows=\"10\"/> </textarea><br>");
  document.write("<button id=\"button_invio\" class = \"btn3\" onclick=\"add_data(data.value,contenuto.value);this.innerHTML='ok';\"></button>");
}
selectStudent();
// =============================================================================

  
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