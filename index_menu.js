let imgcnt = 0;
function addLink(textNode, address, img_address="", img_width="150"){
  ++imgcnt;    
  // a
  var linkText = document.createTextNode(" " + textNode);
  var a = document.createElement('a');
  a.style.fontSize = "24px";
  a.style.opacity = .8;
  a.style.color = 'black';
  a.style.background = 'white';
  a.appendChild(linkText);
  a.title = textNode;
  a.href = address;
  let divContent = document.createElement('div');
  divContent.setAttribute('onclick', 'location.href = "' + address + '"');
  divContent.setAttribute("style","cursor:pointer;");
  divContent.id = "myDivId" + imgcnt;
  divContent.classList.add('my');
  divContent.style.backgroundImage = "url('" + img_address + "')";
  divContent.style.backgroundSize = "100% 100%";
  var br = document.createElement('br');
  a.appendChild(br);
  let body = document.querySelector('body');
  divContent.appendChild(a);
  body.appendChild(divContent);
}

function creaDrop(nome, arr_links){
  // funzione che prende un nome e la lista con link e nomi dei link per creare un drop menu in menuDiv
  let contenitore_links = "";
  for (let l in arr_links){
        if (arr_links[l][0].includes(".")){
    contenitore_links += "<li><a href='" + arr_links[l][0] + "'>" + arr_links[l][1] + "</a></li>"
        }
    else {
        contenitore_links += "<li><a href='" + arr_links[l][1] + "'>" + arr_links[l][0] + "</a></li>"
        }
  }
  // inseriamo nome e indirizzi  
  let drop = `<li class="dropdown"><a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">` +  nome + `<span class="caret"></span></a><ul class="dropdown-menu">
            ` + contenitore_links + `</ul></li>`
  return drop
}

  // Creazione variabili drop down da inserire in menuDiv in basso - Esercizi, Moduli, classi

// Here are the data of the different drop down menu that appears on the menu bar, give them any name, it does not matter
let modules = {dropModuli : creaDrop("Appunti", [
  ["La costituzione (benigni)","benigni.html"],
  ["La Costituzione commentata", "https://docs.google.com/document/d/1jctsFNOR1WVUZLiINAga_1rRlx7l0cOnMQKUcaV0OLk/edit"],
  ["I primi 12 articoli", "https://cdn.glitch.com/6f5b6850-3bb1-4610-8137-6eaec273f126%2FCostituzione_3.pdf?1555844864127"],
  ["Marketing - Sintesi", "https://quinta.glitch.me/appunti/marketing.html"],
  ["Marketing mix: presentazione","https://cdn.glitch.com/6f5b6850-3bb1-4610-8137-6eaec273f126%2Fmarketing_mix_slides.pdf?1552021626604"],
  ["Marketing plan (con es)","https://quinta.glitch.me/lettura_marketing_plan.html"],
  ["Budget","https://quinta.glitch.me/breve/budget.html"],
  ["Marketing e Business plan","https://quinta.glitch.me/ebook/businessplan.html"],
  ]),

dropEsercizi : creaDrop("Kahoot", [
  ["Marketing","https://play.kahoot.it/#/?quizId:d3ab1d61-1c43-48a6-886c-6505eb343cd5"]
  ]),

dropRM : creaDrop("Esercizi e Test RM", [
  ["Budget 21 domande (RM)","https://quinta.glitch.me/darm/budget.html"],
  ["Marketing 1(RM)","https://quinta.glitch.me/darm/marketing_swot.html"],
  ["Marketing 2 (RM)","https://quinta.glitch.me/test/marketing24.html"],
  ["Budget esercizio 1","https://quinta.glitch.me/lettura/eserciziobudget1.html"],
  ["Esercitazione Marketing plan","https://quinta.glitch.me/ebook/pianificazione.html"]
  ]),

dropCompiti : creaDrop("Compiti", [
  ["Budget 100 coperti","https://cdn.glitch.com/6f5b6850-3bb1-4610-8137-6eaec273f126%2FBudget_100coperti.pdf?1553270352957"],
  ]),

dropLive : creaDrop("Esercizi LIVE", [
  ["Esercizi Live","https://quinta.glitch.me/firebase/client.html"],
  ["Punteggi","https://quinta.glitch.me/firebase/punteggi.html"]
  ]),
               
dropClassi : creaDrop("Classi", [
  ["3BS","https://terza.glitch.me"],
  ["4BS","https://quarta.glitch.me"],
  ["5BS","https://quinta.glitch.me"]
  ]),               
}

// Takes all the data and pack then into dropHtml string
let dropHtml = "";
for (let m in modules){
 dropHtml += modules[m]; 
}


// Titolo che compare subito sotto il menu + due frasi
let websitename = "5BS";
let homelink = "https://quinta.glitch.me";

// You do not need to change anything down here, because it is all fixed above
menuDiv.innerHTML += `
<nav class="navbar navbar-inverse navbar-fixed-top">
  <div class="container-fluid">
    <div class="navbar-header">
      <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>                        
      </button>
      <a class="navbar-brand" href="`+homelink+`">`+websitename+`</a>
    </div>
    <div class="collapse navbar-collapse" id="myNavbar">
      <ul class="nav navbar-nav">
<!--
        <li class="active"><a href="`+homelink+`">Home</a></li>
-->    
<li class="dropdown">
        `+dropHtml+`
        </li>
      </ul>
    </div>
  </div>
</nav>
`;