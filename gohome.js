// Creating a div element
var divElement = document.createElement("Div");
divElement.id = "divID";

// Styling it
divElement.style.position = "fixed";
divElement.style.top = "5px";
divElement.style.left = "10px";
divElement.style.textAlign = "center";
divElement.style.fontWeight = "bold";
divElement.style.fontSize = "smaller";
divElement.style.paddingTop = "15px";

/* Adding a paragraph to it
var paragraph = document.createElement("P");
var text = document.createTextNode("Ciao");
paragraph.appendChild(text);
divElement.appendChild(paragraph);*/

var img = document.createElement("img");
img.src = "https://cdn.glitch.com/6f5b6850-3bb1-4610-8137-6eaec273f126%2Fimage.png?1549872436615";
var a = document.createElement('a');
var linkText = document.createTextNode("Home");
a.appendChild(img);
a.title = "my title text";
a.href = "index.html";
img.width = 50;
divElement.appendChild(a);

/* Adding a button, cause why not!
var button = document.createElement("Button");
button.style.opacity = .5;
var textForButton = document.createTextNode("Home");
button.appendChild(textForButton);
button.addEventListener("click", function(){
	location.href="index_teoria.html";
});
divElement.appendChild(button);
*/
document.getElementsByTagName("body")[0].appendChild(divElement);
// Appending the div element to body