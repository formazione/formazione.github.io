jQuery.loadScript = function (url, callback) {
    jQuery.ajax({
        url: url,
        dataType: 'script',
        success: callback,
        async: true
    });
} 

if (typeof someObject == 'undefined') $.loadScript('https://quarta.glitch.me/dropdownclassi.js', function(){
    //Stuff to do after someScript has loaded
});

////////////////////////////// altro metodo

body = document.querySelector("body");
var script = document.createElement("script")
script.src = "https://quarta.glitch.me/dropdownclassi.js";
body.append(script);


//// trasformazione in funzione del codice precedente

function scriptSrc(file){
  body = document.querySelector("body");
  var script = document.createElement("script")
  script.src = file;
  body.append(script);
}

scriptSrc("https://quarta.glitch.me/dropdownclassi.js")