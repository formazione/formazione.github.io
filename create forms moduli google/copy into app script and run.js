function createObesityQuizForm() {

  // CAMBIATE IL TITOLO QUI SOTTO AL POSTO DEL TITOLO TRA VIRGOLETTE
  var form = FormApp.create('Test sul Past tense');

  // Transform the form into a quiz
  form.setIsQuiz(true);

// CAMBIATE LE DOMANDE, METTENDOLE COME LE VEDETE NELL'ESEMPIO
// FATELO FARE A CHAT GPT, COSI' NON LE DOVETE SCRIVERE VOI E POI
// LE INCOLLATE
  var questionString = `
Sono andato a scuola.
*I went to school.
I am going to school.
I will go to school.

Qual è la forma corretta del verbo "to be" al past tense per "they"?
*They were
They was
They will be
They are

Quale di queste frasi usa correttamente il past tense?
I see the movie.
I will see the movie.
I am seeing the movie.
*I saw the movie.

Qual è la forma negativa corretta del past tense del verbo "to go"?
I don't go.
I am not going.
I didn't went.
*I didn't go.

Quale frase descrive correttamente un'azione che era abituale nel passato?
I am used to play football.
I will play football.
I am playing football.
*I used to play football.
`;

  var questionsAndAnswers = parseQuestions(questionString);

  // Add questions to the form
  for (var i = 0; i < questionsAndAnswers.length; i++) {
    var item = form.addMultipleChoiceItem();
    var choices = [];
    for (var j = 0; j < questionsAndAnswers[i].choices.length; j++) {
      if (j === questionsAndAnswers[i].correctAnswer) {
        choices.push(item.createChoice(questionsAndAnswers[i].choices[j], true));
      } else {
        choices.push(item.createChoice(questionsAndAnswers[i].choices[j], false));
      }
    }
    item.setTitle(questionsAndAnswers[i].question)
        .setChoices(choices)
        .setPoints(1)
        .setRequired(true);
  }

  form.setConfirmationMessage('Grazie per aver completato il quiz sull\'obesità!');
  form.setAllowResponseEdits(false);
  form.setCollectEmail(true);
}

function parseQuestions(questionString) {
  var questionsArray = questionString.trim().split('\n\n');
  var questionsAndAnswers = questionsArray.map(function(questionBlock) {
    var lines = questionBlock.split('\n');
    var question = lines[0];
    var choices = lines.slice(1);
    var correctAnswerIndex = choices.findIndex(choice => choice.startsWith('*'));
    choices[correctAnswerIndex] = choices[correctAnswerIndex].slice(1); // Remove the '*' from the correct answer

    return {
      question: question,
      choices: choices,
      correctAnswer: correctAnswerIndex
    };
  });

  return questionsAndAnswers;
}

function setup() {
  createObesityQuizForm();
}
