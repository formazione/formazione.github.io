// Creating a div element
var divEl2 = document.createElement("Div");
divEl2.id = "div2";

// Styling it
divEl2.style.position = "fixed";
divEl2.style.top = "70px";
divEl2.style.left = "10px";
divEl2.style.textAlign = "center";
divEl2.style.fontWeight = "bold";
divEl2.style.fontSize = "smaller";
divEl2.style.paddingTop = "15px";

/* Adding a paragraph to it
var paragraph = document.createElement("P");
var text = document.createTextNode("Ciao");
paragraph.appendChild(text);
divEl2.appendChild(paragraph);*/

function link(text, address){
  if (document.location.href != address){
    let a2 = document.createElement('a');
    let linkText = document.createTextNode(text);
    a2.title = text;
    a2.href = address;
    a2.appendChild(linkText);
    img.width = 50;
    divEl2.appendChild(a2);
    let br = document.createElement('br');
    divEl2.appendChild(br);
  }
}

link("Esercizi","https://terza.glitch.me/index_esercizi.html");
link("Teoria","https://terza.glitch.me/index_teoria.html");

/* Adding a button, cause why not!
var button = document.createElement("Button");
button.style.opacity = .5;
var textForButton = document.createTextNode("Home");
button.appendChild(textForButton);
button.addEventListener("click", function(){
	location.href="index_teoria.html";
});
divEl2.appendChild(button);
*/
document.getElementsByTagName("body")[0].appendChild(divEl2);
// Appending the div element to body