
esercizio = """
<!--- Esercizio 1 -->
  <div style="color:yellow">

<!-- Traccia -->
[traccia]

</div>


<!-- Merci c/acquisti -->
  <table border=1 style="width:300">
  <td colspan=2><center>

Merci c/acquisti</center><tr>

  <td  style="width:150">
<input type="text" id="i1" style="width:150" value=0></td><td style="width:150">
<input type="text" id="i2" style="width:150" value=0></td>
  </table><br><br> <!-- Fine conto Merci c/acquisti-->


<!-- Conto IVA a Credito -->
  <table border=1 style="width:300">
  <td colspan=2><center>

IVA a credito v/Stato</center><tr>

  <td  style="width:150">
<input type="text" id="i3" style="width:150" value=0></td><td style="width:150">
<input type="text" id="i4" style="width:150" value=0></td>
  </table><br><br> <!-- Fine conto Iva a credito-->

<!-- Debiti v/fornitori-->
  <table border=1 style="width:300">
  <td colspan=2><center>

Debiti v/fornitori</center><tr>

  <td  style="width:150">
<input type="text" id="i5" style="width:150" value=0></td><td style="width:150">
<input type="text" id="i6" style="width:150" value=0></td>
  </table><br><br> <!-- Fine conto Iva a credito-->




<!-- <br><br>   PULSANTE PER INVIO DELLE RISPOSTE --->
<!-- <button id="c1" onclick="inp1.value='Merci c/acquisti: ' + i1.value+' avere:' + i2.value + '\nIva a credito: dare: ' + i3.value + ' avere:' + i4.value + '\nDebiti v/fornitori dare: ' + i5.value + ' avere: ' + i6.value">Invia risposte del test</button> --> -->

<button id="c2" onclick="if(i1.value=='100' && i2.value=='0' && i3.value=='22' && i4.value=='0' && i5.value=='0' && i6.value=='122'){ver1.value='esatto'}else{ver1.value='sbagliato'};console.log(i1.value);">Verifica risposte</button>

<input id="ver1">"""

darecount = 1
averecount = 1
testo = ""
sol = ""
obj_input_name = []
def conto(titolo, dare="0", avere="0"):
  global testo, sol, darecount, averecount

  testo += f"""<!-- {titolo} -->
  <table border=1 style="width:300">
  <td colspan=2><center>{titolo}</center><tr>
  <td  style="width:150">
<input type="text" id="dare{darecount}" style="width:150" value=0></td><td style="width:150">
<input type="text" id="avere{averecount}" style="width:150" value=0></td>
  </table><br><br> <!-- Fine conto {titolo}-->
"""
  sol += f"{dare} {avere} "
  obj_input_name.append([f"dare{darecount}.value", f"avere{averecount}.value"])
  darecount +=1
  averecount +=1
  '''
  ogni volta che crei un conto aggiungi a sol il dare e avere giusti, così per
  controllare che la soluzione sia giusta, crea una stringa con gli input
  dell'utente e confrontala con la stringa sol contenente la soluzione.

  '''
  return testo
stringa = ""
def stringa_input():
  global testo, sol, stringa

  stringa = ""
  for d,a in obj_input_name:
    stringa += f"{d} + ' ' + {a} + ' ' + "
  stringa = stringa[:-9]
  testo += f"""<button onclick="if ({stringa}=='{sol}'){{ver1.value='giusto'}}else{{ver1.value='sbagliato'}}; console.log({stringa});console.log('{sol}');">Verifica risposte</button><input id='ver1' type='text'>"""
  return stringa


def tag(_t, testo):
  return f"<{_t}>{testo}</{_t}>"

# ====== | TRACCIA | ====== #
traccia = "Pagata in contanti fattura di acquisto merci emessa in precedenza per 1.500 euro. Abbiamo meno denaro in cassa e meno debiti nel conto debiti v/fornitori."
# ogni volta che crei un conto si aggiunge la stringa col codice a testo
conto("Debiti v/fornitori", "1.500", "0")
conto("Denaro in cassa", "0", "1.500")

# alla fine salva un file col testo
sol = sol[:-1]
stringa_input()
testo = tag("h3", "Esercizio") + tag("p",traccia) + testo
print(testo)
