function textNButton(num, testoparlato, titolo){
  // testo parlato deve avere una domanda con ? e poi la risposta
  // mostra il testo seguito da un pulsante per leggerlo
  let risposta = testoparlato.split("?")[1];
  let domanda = testoparlato.split("?")[0] + "?";

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