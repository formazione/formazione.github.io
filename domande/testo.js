
function h(div, testo, h1){
  div.innerHTML += "<" + h1 + ">" + testo + "</" + h1 +">";
}

function p(div, testo){
  div.innerHTML += testo;
}


h(testo1, "I marchi di qualità alimentare", "h1")
p(testo1, "Ciao")