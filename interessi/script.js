function check(id, esatta, counter) {
  // checks if the input is correct
  console.log("id=")
  console.log(esatta)
  console.log(id == esatta)
  div = document.getElementById("div"+counter);
  
  if ((id == esatta) || (esatta.split(" ").includes(id))) {
    // alert("Giusto");
    div.innerHTML = "Giusto";
  }
  else {
    // alert("No" + id);
    div.innerHTML = "No";
  }
};

counter = 0
function dom(questione, risposta) {
  html = `
  <!-- DOMANDA 1 -->
1. ` + questione + `
<input id="q` + counter + `" class="txtb" type="text" onchange="check(q`+ counter + `.value, '` + risposta + `', `+counter+`)"><br>
<button id="verify" onclick="check(q`+ counter + `.value, '` + risposta + `', `+counter+`)">Verifica le risposte</button><br>
<div id="div`+counter+`"></div>

<br>
`
  document.write(html);
  console.log(risposta);
  counter += 1

}