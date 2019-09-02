  var config = {
    apiKey: "AIzaSyDp-mWaWEI07pIdRUhi6vA-salEMRWz4hw",
    authDomain: "quiz-e5e5a.firebaseapp.com",
    databaseURL: "https://quiz-e5e5a.firebaseio.com/",
    projectId: "quiz-e5e5a",
    storageBucket: "quiz-e5e5a.appspot.com",
    messagingSenderId: "901845403492"
  };
  firebase.initializeApp(config);
  var database = firebase.database()
  var dbref1 = database.ref().child("notebook");
  function add_data(d,c){
    dbref1.child(d).set(c)
  }
ref1 = database.ref()