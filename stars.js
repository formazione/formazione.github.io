//var canvas = document.querySelector('canvas');
//  ----------------- CANVAS ------------------
let canvas = document.createElement('canvas');
ww = window.innerWidth;
wh = window.innerHeight;
canvas.width = ww;
canvas.height = wh;
canvas.style.position = "absolute";
canvas.style.top = "0";
canvas.style.zIndex = "-2";
let body = document.querySelector('body');
body.appendChild(canvas);
// ------------------------------------------- canvas

var c = canvas.getContext('2d');

function rnd(x){
  // returns a random number from 1 to 10 if x=1
 return Math.floor(Math.random()*x); 
}

function rndFromArray(x){
  // x è un array che viene mischiato e restituito
    x.sort(function() {
      return .5 - Math.random();
    });
  return x[0];}

colors = ["white","gold","coral","red","lime","blue","cyan","black","gray","maroon"];

function rndrgba(){
	// creates a random color transparent
	a1 = rnd(255);
	a2 = rnd(255);
	a3 = rnd(255);
	rnd_rgba = "rgba(" + a1 + "," + a2 + "," + a3 + ", 0.5)";
	return rnd_rgba;
}

let text = ["Hello","Ciao","See ya","Bonjour","Tschus","Hola","Salut","Hallo","Vitaj","Haloo"]; 
function addText(x,y){
      c.font = 10 + rnd(30) + "px Arial";
      c.fillText(rndFromArray(text)[0], x, y);
}

function circle(x,y,w){
      c.beginPath();
      c.arc(x, y, w*rnd(5), 0, 2 * Math.PI);
      c.fillStyle = rndrgba();
      c.fill();
}


let pianeta = new Image();
let lista_img = ["https://cdn.glitch.com/1e8a1dde-7ab4-43db-8ec8-1ccb6d3cad7f%2Fimage.png?1549225555086",
"https://cdn.glitch.com/1e8a1dde-7ab4-43db-8ec8-1ccb6d3cad7f%2Fimage.png?1549225487544",
                 "https://cdn.glitch.com/1e8a1dde-7ab4-43db-8ec8-1ccb6d3cad7f%2Fimage.png?1549225851682",
                 "https://cdn.glitch.com/1e8a1dde-7ab4-43db-8ec8-1ccb6d3cad7f%2Fimage.png?1549224536516",
                 "https://cdn.glitch.com/1e8a1dde-7ab4-43db-8ec8-1ccb6d3cad7f%2Fimage.png?1549471639092"
                ];
function addImage(x,y){
  let random_planet = rnd(lista_img.length);
  pianeta.src = lista_img[random_planet];
  w = 10 + rnd(50);
  h = w;
  c.globalAlpha = rnd(10)/10;
  c.translate( c.width/2 , c.height/2 );
  c.rotate(90);
  c.drawImage(pianeta,x,y,w,h);
  
}

function randomCircles(){
			x = rnd(ww);
			y = rnd(wh);
			w = rnd(10);
			h = rnd(10);
  if (rnd(2)==0){
    c.globalAlpha = 1;
        circle(x,y,w)
      }
  else {
    //addText(x,y);
        addImage(x,y);
  }
	  // c.fillStyle = rndclr(colors)[0];
	  //c.fillRect(x, y, w*rnd(5), h*rnd(5));
}


function randomRectangles(){
			x = rnd(ww);
			y = rnd(wh);
			w = rnd(10);
			h = rnd(10);
			// c.fillStyle = rndclr(colors)[0];
      c.fillStyle = rndrgba();
			c.fillRect(x, y, w*10, h*10);
	
}

setInterval(function(){randomCircles();}, 100);