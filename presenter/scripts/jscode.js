var quiztitle = "Hotel";

function speak(x, language="it") {
  synth = speechSynthesis
  utt = new SpeechSynthesisUtterance(x);
  utt.lang=language;
  synth.speak(utt);
  is_on = 1;
}


function shuffle(array) {
  var currentIndex = array.length, temporaryValue, randomIndex;
  // While there remain elements to shuffle...
  while (0 !== currentIndex) {
    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;
    // And swap it with the current element.
    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }
  return array;
}
	    
if (!("scramble" in Array.prototype)) {
  Object.defineProperty(Array.prototype, "scramble", {
    enumerable: false,
    value: function() {
      var o, i, ln = this.length;
      while (ln--) {
        i = Math.random() * (ln + 1) | 0;
        o = this[ln];
        this[ln] = this[i];
        this[i] = o;
      }
      return this;
    }
  });
}		


quiz.forEach(q => q.choices.scramble()); // Mescola l'ordine delle risposte
quiz = shuffle(quiz);
var currentquestion = 0, score = 0, submt=true, picked;
let count_speak = 0;
jQuery(document).ready(function($){

  
function addChoices(choices){
		if(typeof choices !== "undefined" && $.type(choices) == "array"){
			$('#choice-block').empty();
			for(var i=0;i<choices.length; i++){
        // added .css({'font-size':'36px'}) il 2 marzo 2019
			$(document
        .createElement('li'))
        .addClass('choice choice-box btn')
        .attr('data-index', i)
        .text(choices[i])
        .appendTo('#choice-block')
        .css({'font-size':'28px'});		//  Aggiunge risposte
      }
		}
      
	}
        

function nextQuestion(){
   
		submt = true;
		$('#explanation').empty(); // svuota spiegazione
		$('#question').text(quiz[currentquestion]['question']); // domanda attuale
    // domanda n. di ... totale domande
		$('#pager').text('Domanda' + Number(currentquestion + 1) + ' di ' + quiz.length);
    // Immagine... ?
		if(quiz[currentquestion].hasOwnProperty('image') && quiz[currentquestion]['image'] != ""){
			if($('#question-image').length == 0){
				$(document.createElement('img'))
          .addClass('question-image')
          .attr('id', 'question-image')
          .attr('src', quiz[currentquestion]['image'])
          .attr('alt', (quiz[currentquestion]['question']))
          .insert('#question');
			} else {
				$('#question-image')
          .attr('src', quiz[currentquestion]['image'])
          .attr('alt', (quiz[currentquestion]['question']));
			}
		} else {
			$('#question-image')
        .remove();
		}
		addChoices(quiz[currentquestion]['choices']);
		setupButtons();
		// parla solo una volta ======|||||||||=====>>>
          if (count_speak==0 && is_on==1){
      speak(quiz[currentquestion]['question']);
      count_speak = 1;
    }
      } // function nextQuestion


function processQuestion(choice){
  
  // ===========   Risposta ESATTA!  ==============================
  if(quiz[currentquestion]['choices'][choice] == quiz[currentquestion]['correct'])
    {
			$('.choice')
        .eq(choice)
        .addClass('btn-success')
        .css({'font-size':'36px', 'font-weight':'bold', 'border-color':'#51a351', 'color':'#fff'});
			$('#explanation')
        .html('<span class="correct">ESATTO!</span> ' + (quiz[currentquestion]['explanation']));
            let ff = ["sì","ok","bene","sicuro","corretto","esatto","perfetto","certo","giusto",].sort(function(){return 0.5 - Math.random()})[0];
      speak(ff);
			      score++;
            count_speak = 0;
		} 
    
  else {
    $('.choice')
          .eq(choice)
          .addClass('btn-danger')
          .css({'font-weight':'bold', 'border-color':'#f93939', 'color':'#fff'});
    $('#explanation')
      .html('<span class="incorrect">INESATTO!</span> ' + (quiz[currentquestion]['explanation']));
      speak("No! è")
      // francese
      speak(quiz[currentquestion]['correct'], LINGUA_RISPOSTA); // RISPOSTA ERRATA IN LINGUA FRANCESE
          }
      count_speak = 0;
      currentquestion++;
  // ========================= qui è stata aggiunta da 322
  if (currentquestion < quiz.length)  nextQuestion();
  // =========================


    // SONO FINITE LE DOMANDE... MOSTRA I RISULTATI
	if(currentquestion == quiz.length){
		$('#submitbutton')
      .html('GET QUIZ RESULTS') // nuovo testo
      .removeClass('btn-success') // nuovo stile
      .addClass('btn-info')
      .css({'border-color':'#3a87ad', 'color':'#fff'})
      .on('click', function(){$(this).text('GET QUIZ RESULTS').on('click');
			endQuiz();
		})
		
	}
    
    else if (currentquestion < quiz.length)
    {} 
    // SE CI SONO ANCORA DOMANDE, RIMETTE IL PULSANTE CONTROLLA LA RISPOSTA
      
			// $('#submitbutton').html('VAI ALLA PROSSIMA DOMANDA &raquo;')
      //   .removeClass('btn-success')
      //   .addClass('btn-warning')
      //   .css({'font-weight':'bold', 'border-color':'#faa732', 'color':'#fff'})
      //   .on('click', function(){
			// 	        $(this).text(' CLICCA PRIMA SUL PULSANTE QUI SOPRA ')
			//           .removeClass('btn-warning')
			//           .addClass('btn-success')
			//           .css({'font-weight':'bold', 'border-color':'#51a351', 'color':'#fff'})
			//           .on('click');
			// 	        nextQuestion();})
      // }
		
	}

     

let LINGUA_RISPOSTA = "fr"; // cambia la lingua della risposta quando le lingue sono diverse

function setupButtons(){
    //speak(quiz[currentquestion]['question'])
		$('.choice').on('click', function(){
		synth.cancel();
    is_on = 0;
		picked = $(this).attr('data-index');
		speak(quiz[currentquestion]['choices'][picked], LINGUA_RISPOSTA);
		show_button();
		// risposte in francese
		$('.choice').removeAttr('style').off('mouseout mouseover');
		$(this).css({'font-weight':'900', 'border-color':'#51a351', 'color':'#51a351', 'background' : 'gold'});
		if(submt){
				submt=false;
				$('#submitbutton').css({'color':'#fff','cursor':'pointer'}).on('click', function(){
				$('.choice').off('click');
				$(this).off('click');
				processQuestion(picked);
          //
				});
			}
		})
	}
      
      
function endQuiz(){
		$('#explanation').empty();
		$('#question').empty();
		$('#choice-block').empty();
		$('#submitbutton').remove();
		$('.rsform-block-submit').addClass('show');
		$('#question').text("You got " + score + " out of " + quiz.length + " correct.");
		$(document.createElement('h4')).addClass('score').text(Math.round(score/quiz.length * 100) + '%').insertAfter('#question');			
	}

      /**
       * Runs the first time and creates all of the elements for the quiz
       */
	function init(){
    speak(quiz[currentquestion]['question'])
		//add title
 
		if(typeof quiztitle !== "undefined" && $.type(quiztitle) === "string"){
			$(document.createElement('h2')).text(quiztitle).appendTo('#frame');
		} else {
			$(document.createElement('h2')).text("Quiz").appendTo('#frame');
		}
 
		
		//add pager and questions
		if(typeof quiz !== "undefined" && $.type(quiz) === "array"){
			//add pager
      
			$(document.createElement('p')).addClass('pager').attr('id','pager').text('Domanda 1 di ' + quiz.length).appendTo('#frame');
			//add first question
			$(document.createElement('h3')).addClass('question').attr('id', 'question').text(quiz[0]['question']).appendTo('#frame');
			//add image if present
			if(quiz[0].hasOwnProperty('image') && quiz[0]['image'] != ""){
				$(document.createElement('img')).addClass('question-image').attr('width','100px').attr('id', 'question-image').attr('src', quiz[0]['image']).attr('alt', (quiz[0]['question'])).appendTo('#frame');
			}
			
			$(document.createElement('p')).addClass('explanation').attr('id','explanation').html('').appendTo('#question');
			
			//questions holder
			$(document.createElement('ul')).attr('id', 'choice-block').appendTo('#frame');
			
			//add choices
			addChoices(quiz[0]['choices']);
			
			
			setupButtons();
		}
	}

function show_button(){
			//add submit button
			$(document.createElement('div')).addClass('btn-success choice-box').attr('id', 'submitbutton').text('- CONTROLLA LA RISPOSTA -').css({'font-weight':'bold', 'color':'#fff','padding':'30px 0', 'border-radius':'10px'}).appendTo('#frame').on('click');
}

	init();

});
		
// function copyText() {
// 	var output = document.getElementById("frame").innerHTML;
// 	document.getElementById("placecontent").value = output;
// }
