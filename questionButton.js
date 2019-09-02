function speak(x) {
  speechSynthesis.speak(new SpeechSynthesisUtterance(x));
}
console.log("Il secondo argomento deve avere una domanda con ? e poi la risposta");
function questionButton(num, qnr, titolo){
  // qnrdeve avere una domanda con ? e poi la risposta
  // mostra il testo seguito da un pulsante per leggerlo
  let risposta = qnr.split("?")[1];
  let domanda = qnr.split("?")[0] + "?";

  // 1. Create the button ============================= BUTTON
  var button = document.createElement("button");
  button.innerHTML = domanda; // the value of the button
  // 2. Append somewhere
  var body = document.getElementsByTagName("body")[0];
  body.appendChild(button);

  // 3. Add event handler
  button.addEventListener ("click", function() {
    speak(risposta);
    button.innerHTML = domanda + "<br><span style='font-size:16px; color:gold'>" + risposta + "</span>";
  });
}

// Esempio con link nella risposta
//questionButton(1, "Vuoi andare al prossimo esercizio? <a href='3bs_es2.html'>Clicca qui</a>", "Es. 2");