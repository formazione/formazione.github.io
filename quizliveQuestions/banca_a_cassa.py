<!--- Esercizio 1 -->
  <div style="color:yellow">

Spostati 100 euro dalla Cassa alla Banca</div>

  <table border=1 style="width:300">
  <td colspan=2><center>

banca x c/c</center><tr>

  <td  style="width:150">
<input type="text" id="i1" style="width:150"></td><td style="width:150">
<input type="text" id="i2" style="width:150"></td>
  </table><br><br> <!-- Fine esercizio -->

  <table border=1 style="width:300">
  <td colspan=2><center>

Denaro in cassa</center><tr>

  <td  style="width:150">
<input type="text" id="i3" style="width:150"></td><td style="width:150">
<input type="text" id="i4" style="width:150"></td>
  </table><br><br> <!-- Fine esercizio -->


<br><br> <!--      PULSANTE PER INVIO DELLE RISPOSTE --->
<button id="c1" onclick="inp1.value='Banca x c/c dare: ' + i1.value+' avere:' + i2.value + '\nDenaro in cassa: dare: ' + i3.value + ' avere:' + i4.value">Invia risposte del test</button>