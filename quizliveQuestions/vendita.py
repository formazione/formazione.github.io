<h3>Esercizio</h3><p>Ricevuta fattura di acquisto per 500 € + 10% di IVA</p><!-- Merci c/acquisti -->
  <table border=1 style="width:300">
  <td colspan=2><center>Merci c/acquisti</center><tr>
  <td  style="width:150">
<input type="text" id="dare1" style="width:150" value=0></td><td style="width:150">
<input type="text" id="avere1" style="width:150" value=0></td>
  </table><br><br> <!-- Fine conto Merci c/acquisti-->
<!-- Iva a credito -->
  <table border=1 style="width:300">
  <td colspan=2><center>Iva a credito</center><tr>
  <td  style="width:150">
<input type="text" id="dare2" style="width:150" value=0></td><td style="width:150">
<input type="text" id="avere2" style="width:150" value=0></td>
  </table><br><br> <!-- Fine conto Iva a credito-->
<!-- Debiti v/fornitori -->
  <table border=1 style="width:300">
  <td colspan=2><center>Debiti v/fornitori</center><tr>
  <td  style="width:150">
<input type="text" id="dare3" style="width:150" value=0></td><td style="width:150">
<input type="text" id="avere3" style="width:150" value=0></td>
  </table><br><br> <!-- Fine conto Debiti v/fornitori-->
<h3>Esercizio 2</h3><p>Pagato in contanti fattura precedente</p><!-- Debiti v/fornitori -->
  <table border=1 style="width:300">
  <td colspan=2><center>Debiti v/fornitori</center><tr>
  <td  style="width:150">
<input type="text" id="dare4" style="width:150" value=0></td><td style="width:150">
<input type="text" id="avere4" style="width:150" value=0></td>
  </table><br><br> <!-- Fine conto Debiti v/fornitori-->
<!-- Denaro in cassa -->
  <table border=1 style="width:300">
  <td colspan=2><center>Denaro in cassa</center><tr>
  <td  style="width:150">
<input type="text" id="dare5" style="width:150" value=0></td><td style="width:150">
<input type="text" id="avere5" style="width:150" value=0></td>
  </table><br><br> <!-- Fine conto Denaro in cassa-->
<button onclick="if (dare1.value + ' ' + avere1.value + ' ' + dare2.value + ' ' + avere2.value + ' ' + dare3.value + ' ' + avere3.value + ' ' + dare4.value + ' ' + avere4.value + ' ' + dare5.value + ' ' + avere5.value=='500 0 50 0 0 550 550 0 0 550'){ver1.value='giusto'}else{ver1.value='sbagliato'}; console.log(dare1.value + ' ' + avere1.value + ' ' + dare2.value + ' ' + avere2.value + ' ' + dare3.value + ' ' + avere3.value + ' ' + dare4.value + ' ' + avere4.value + ' ' + dare5.value + ' ' + avere5.value);console.log('500 0 50 0 0 550 550 0 0 550');">Verifica risposte</button><input id='ver1' type='text'>
[hoops name='all']
>>> 