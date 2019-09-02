function dark_theme(){
  document.write("<html><head><style>");
  document.write("body { font-size:2em; color:white; background:black;}");
  document.write("a{color:lime;} a:visited { color:orange;  }");
  document.write("</style></head>");
  document.write("<body onkeydown='arrowlefthome(event.key)'>");
 }

function arrowlefthome(key){
  // go back to home page
  // Go back home when hit arrow key, see body onkeydown action... do we need an EventListener?
  if (key == "ArrowLeft"){
         window.location.href = "index.html";}
}


function gobackhome(){
  // TASTO HOME
  document.write("<a href='index.html'>HOME</a><br>");
}


function createpage(title, content){
  // dark theme
  dark_theme();
  // TASTO HOME
  gobackhome();
  // TITOLO
  document.write("<div class='container'>");
  document.write("<h3>"+ title + "</h4>");
  // CONTENUTO DELLA PAGINA CREATA  
  document.write("<p>" + content + "</p>");
  document.write("</div>");
  document.write("</body></html>");
}

