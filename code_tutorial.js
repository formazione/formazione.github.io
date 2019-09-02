/*
INDEX - Examples of functions for various purposes
  regular expressions
  voice
  
*/
let index = {
  "regex(x)" : "finds all the words starting with #",
  "speak(f)" : "makes the computer speak"
};

for (v in index){
 console.log(index[x]); 
}
// =================  REGEX  ====================  \\  

function regex(x){
 // returns all the matches (words that starts with #) in a string and the string formatted
  let words = x.match(/#\w*/g)
    for (n in words){
      x = x.replace(words[n], "<b style='color:yellow'>" + words[n] + "</b>");
      x = x.replace("#","");
  return [words,x];
    }
}
regex("All I need is #love");
// output
// console.log(x)
// ['#love']

// =================  voice  ====================  \\  

function speak(speech){
  const message = new SpeechSynthesisUtterance(speech); 
  window.speechSynthesis.speak(message);
}