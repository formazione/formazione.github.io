var config = {
  apiKey: "AIzaSyDp-mWaWEI07pIdRUhi6vA-salEMRWz4hw",
  authDomain: "quiz-e5e5a.firebaseapp.com",
  databaseURL: "https://quiz-e5e5a.firebaseio.com/",
  projectId: "quiz-e5e5a",
  storageBucket: "quiz-e5e5a.appspot.com",
  messagingSenderId: "901845403492"
};
firebase.initializeApp(config);
var database = firebase.database()
var dbref1 = database.ref().child(document.title);
// ===============================================
          
function add_data(d,c,e){
  dbref1.child(d).child(e).set(c)
}

function printnome(num){
  // This creates an input text box with a data+num id for each student -->
  page.innerHTML += "Inserisci il tuo nome:<br><input id='data" + num + "' class='mytext' type=text value='' /><br>";
}

function printtextandbutton(numalunno,num){
  //page.innerHTML += "<input id='data" + num + "' type=text value='' />";
  page.innerHTML += "Risposta " + num + ": <textarea id='contenuto"+ num + "' type='text' rows='3' /></textarea>";
  domanda = "domanda" + num;
  let testo = testo_domanda[num].split(" ").join("").replace("'","`");
  page.innerHTML += "<br><button onclick=add_data(data"+ numalunno + ".value,contenuto" + num +".value,'" + testo + "');>Invia</button><br>";
}

function questionwrite(domanda_fatta){
   page.innerHTML += "<b>" + domanda_fatta + "</b><br>";
}

let testo_domanda = [];
function qmk(domanda_fatta){
  testo_domanda.push(domanda_fatta);
  questionwrite(domanda_fatta);
  printtextandbutton("1",countnum);
  questionwrite("<br>");
  countnum++
  //dbref1.on("value", snap => x = snap.value())
}
      
page.innerHTML += "<h3>Esercizio " + document.title + "</h3>";
      page.innerHTML += "<img src='https://tdm-pull-wol7ynwfkovcdc2im8l.netdna-ssl.com/wp-content/uploads/2011/11/Content-Marketing-Header.jpg' width='100%' />";
printnome("1");
      
let countnum = 0;

  
function createDiv(){
  let ref = firebase.database().ref().child(document.title);
  ref.on('value', function(snapshot) {
    let count = 0;
    snapshot.forEach(function(childSnapshot) {
      let divX = document.createElement("div");
      divX.setAttribute('id', 'al' + count);
      document.body.appendChild(divX),
      count++;})
    }
)};

function retrieveData(){
  
  page2.innerHTML = "";
  let ref = firebase.database().ref().child(document.title);
  
  ref.on('value', function(snapshot) {
      let count1 = 0;
      let snap = snapshot.val();
      for (i in snap){
       console.log("\n" + i);
        // nome dell'alunno =====================
        page2.innerHTML += "<hr>" + i + "<br>";
        // =====================================
        for (n in snap[i]){
             console.log(n, snap[i][n])
              // domanda 1 "risposta" ===========================
              page2.innerHTML += n + " = " + snap[i][n] + "<br>";
              // ================================================
     
      }
  }
  });
}

// password