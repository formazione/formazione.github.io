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
    // puoi mettere sia prima il nome che prima l'indirizzo, ci pensa questo codice a invertirli
        if (arr_links[l][0].includes(".")){
    contenitore_links += "<li><a href='" + arr_links[l][0] + "'>" + arr_links[l][1] + "</a></li>"
        }
    else {
        contenitore_links += "<li><a href='" +  arr_links[l][1] + "'>" + arr_links[l][0] + "</a></li>"
        }
  }
  // inseriamo nome e indirizzi  
  let drop = `<li class="dropdown"><a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">` +  nome + `<span class="caret"></span></a><ul class="dropdown-menu">
            ` + contenitore_links + `</ul></li>`
  return drop
}


let drop_esercizi = creaDrop("Esercizi", [
  ["22 domande sul marketing", "5bs_es1.html" ],
  ["Test contratto ristorativo", "quiz1_ristorazione.html"],
  ["Esercizio sul marketing plan","lettura_marketing_plan.html"],
  ["Pianificazione","https://quinta.glitch.me/test_rm2/vision.html"] 
];)

let drop_moduli = creaDrop("Moduli", [
  [ "Turismo","#"], 
  [ "Marketing", "https://formazione.github.io/bib/i/?book=Marketing.epub"], 
  [ "Business plan", "#"], 
  [ "Contratti", "#"], ];);
let dropClassi = creaDrop("Classi", [
  ["Terza","https://terza.glitch.me"],
  ["Quarta","https://quarta.glitch.me"],
  ["Quinta","https://quinta.glitch.me"]
  ]);
let drop_kahoot = creaDrop("Kahoot", [
  ["Marketing", "https://play.kahoot.it/#/?quizId=f2788dae-ca7b-4588-b662-6b8042d370c7"],
  ["Marketing operativo","https://play.kahoot.it/#/?quizId=db9361af-f907-4316-96d8-712ede1a3fb7"],
  ];); 
// =====================================================================

menuDiv.innerHTML += `
 <!-- Fixed navbar 
-->
    <nav class="navbar navbar-default navbar-fixed-top">
      <div class="container">
        <div class="navbar-header"> 
</div>
        <div id="navbar" class="navbar-collapse collapse">
          <ul class="nav navbar-nav">
                     <!--         HOME BUTTON    -->
            <li><a class="navbar-brand" style="width:100%;float:left;padding:0px;text-align:center;" href="https://quinta.glitch.me"><img src="https://cdn.glitch.com/1e8a1dde-7ab4-43db-8ec8-1ccb6d3cad7f%2Fimage.png?1551073632101" width="50" /></a></li>
            
` + drop_moduli + ` 
` + drop_esercizi + ` 
` + drop_kahoot + dropClassi + ` 
          </ul>   
      </div>
    </nav><br><br><br><br>
<!--
-->
`;