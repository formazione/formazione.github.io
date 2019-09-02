How to add score with firebase database in snake

A. MANUALE

- working in version 1, 9...10

1.
Put this on top of the code
<!-- import the code for firebase -->
<script src="https://www.gstatic.com/firebasejs/4.10.1/firebase.js"></script>
<!-- my configuration of firebase -->
<script src="quiz-e5e5aconfig.js"></script>

2.
This after let rec=0 (change the snake1 to what you need for different versions)
ref1.child("snake1").child("record").on("value", snap => rec = snap.val());

3.
After line 131 put:
              if (sc > rec) {
                  rec = sc;
                  ref1.child("snake1").child("record").set(rec);
              }
              
              
B. HISTORY OF CHANGES
              
              
Versions changes

1. Version snake1.html added circle() function to transform in circle
    added score with firebase, colors for snake with pickRndItem()
    addes sounds (all from the 9 version).
    - added the z control for add partite!
    When you hit the apple in a certain moment you gain 100
    the more long you are, more points you gain
    7.1.19

Version snake1_1
  - You get 100 and you go back to when you were 5 of length and you become gold
  - added morescore variable to increase points when you go on
    morescore:
    - get 10 when eat
    - get -5 when time passes
    - get another 20 when eat fast