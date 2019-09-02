function title(){
 document.write("<h3>Articoli in evidenza</h3>"); 
}

function show(address, title){
  document.write("<a href='" + address + "'>"+title+"</a>");
  document.write(" - ");
}

// page maker - 21/01/2019 - Visualizza titolo e link
title(); // il titolo della sezione della pagina
show('marketing.html','Marketing'); // primo link 21/1/19
