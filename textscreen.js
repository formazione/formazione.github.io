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

let text = ["costi","ricavi","bilancio","utile","gestione","marketing","finanziamenti","immobilizzazioni","produzione","investimenti","debiti","banca","clienti","customer"]; 
function addText(x,y){
      let randomText = rnd(text.length);
      let testo = text[randomText];
      c.font = 10 + rnd(30) + "px Arial";
      c.fillText(testo, x, y);
}

let textMoney = ["€","$"];

function circle(x,y,w){
      c.beginPath();
      c.arc(x, y, w*rnd(5), 0, 2 * Math.PI);
      c.fillStyle = rndrgba();
      c.fill();
}

function money(x,y,w){
      c.beginPath();
      let raggio = 5 + w*rnd(5);
      c.arc(x, y, raggio, 0, 2 * Math.PI);
      c.fillStyle = rndrgba();
      c.fill();
      let random_money = rnd(textMoney.length);
      c.font = raggio + 8 + "px Arial";
      c.fillText(textMoney[random_money], x-6, y+6);
}


let pianeta = new Image();
let lista_img = ["https://www.iconshock.com/image/RealVista/Accounting/payment",
                 
              "https://7icons.files.wordpress.com/2010/08/moneybagpound256.png?w=256&h=256",
                 "http://www.myiconfinder.com/uploads/iconsets/256-256-3b059644cef1d0d58c250a23f9287dce-cash.png",
                 "https://pngimage.net/wp-content/uploads/2018/06/piggy-bank-money-png.png",
                 "https://ya-webdesign.com/images/cash-register-png-9.png"
                ];
let il_testo = ["questo","xxx"];


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

function addText2(x,y){
  let randomText = rnd(il_testo.length);
  let word = document.createTextNode(il_testo[randomText]);
  w = 10 + rnd(50);
  h = w;
  c.globalAlpha = rnd(10)/10;
  c.translate( c.width/2 , c.height/2 );
  c.rotate(90);
  c.font = "30px Arial";
  c.fillText("Hello World", x, y);
  //c.drawImage(pianeta,x,y,w,h);
}


function randomFigures(){
			x = rnd(ww);
			y = rnd(wh);
			w = rnd(10);
			h = rnd(10);
  let chance = rnd(3);
  if (chance==0){
    c.globalAlpha = 1;
    money(x,y,w)
  }
  else if (chance==1){
    //addText(x,y);
    addImage(x,y);
  }
  else {
    addText(x,y);
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

setInterval(function(){randomFigures();}, 50);
// la funzione randomCircle va a circle o addImage casualmente