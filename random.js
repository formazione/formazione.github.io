function rnd(x){
  // x è un array che viene mischiato e restituito
    x.sort(function() {
      return .5 - Math.random();
    });
  return x;};

function random(x){
  // returns a random number from 1 to 10 if x=1
 return Math.floor(Math.random()*10+1)*x; 
}

dati.sort(function() {return .5 - Math.random();});