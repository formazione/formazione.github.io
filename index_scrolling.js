var pointX, pointY , w , h ;

var myCanvas = document.getElementById("myCanvas");
var ctx = myCanvas.getContext("2d");
myCanvas.width = $(window).width(); // larghezza del canvas come la finestra
myCanvas.style.position = "absolute";
myCanvas.height = 160;
//myCanvas.style.background = "yellow";
//ctx.clearRect(0, 0, $(window).width(),ctx.canvas.height);

let start = -350;
 
function frame(){
  requestAnimationFrame(frame)
  ctx.clearRect(0,0,$(window).width(), myCanvas.height)
  start += 2;
  ctx.font = "24px Arial";
  ctx.fillStyle = "whitesmoke";
  ctx.textAlign = "left";
  ctx.fillText("Verifiche orali sul marketing da martedì 19",start, 150); 
  if (start > $(window).width()) start = -350;
  }

frame()