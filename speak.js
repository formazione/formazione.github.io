function speak(x) {
  speechSynthesis.speak(new SpeechSynthesisUtterance(x));
}