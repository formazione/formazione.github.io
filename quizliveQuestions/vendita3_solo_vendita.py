'''
crea esercizi in partita doppia come questo:

https://aziendaitalia.altervista.org/esercizio-in-partita-doppia-sulle-vendite/


'''




def conto(titolo, dare="0", avere="0"):
  global testo, sol, darecount, averecount

  # Creazione del conto in html
  testo += f"""

  <!-- #############  {titolo}  ################  -->


  <table border=1 style="width:300">
  <td colspan=2><center>{titolo}</center><tr>
  <td  style="width:150">

  <!-- ####  D A R E   ######## -->
<input type="text" id="dare{darecount}" style="width:150" value=0></td><td style="width:150">


<!-- #####  A V E R E  ###### -->

<input type="text" id="avere{averecount}" style="width:150" value=0></td>
  </table><br><br> <!-- Fine conto {titolo}-->
"""
  sol += f"{dare} {avere} | "
  obj_input_name.append([f"dare{darecount}.value", f"avere{averecount}.value"])
  darecount +=1
  averecount +=1
  return testo


def pulsante_di_verifica():
  global testo, sol, stringa

  sol = sol[:-1]
  stringa = ""
  for d,a in obj_input_name:
    stringa += f"{d} + ' ' + {a} + ' | ' + "
  stringa = stringa[:-6]
  stringa = stringa + "|'"
  # stringa += "'|'"
  testo += f"""

<!-- ############### VERIFY INPUT ################ -->

  <button onclick="if ({stringa}=='{sol}'){{ver1.value='giusto'}}else{{ver1.value='sbagliato'}};inp1.value={stringa}+' '+ver1.value; console.log({stringa});console.log('{sol}');">Verifica risposte</button><input id='ver1' type='text'>"""
  return stringa


def tag(_t, testo):
  return f"<{_t}>{testo}</{_t}>"




stringa = ""
darecount = 1
averecount = 1
testo = ""
sol = ""
obj_input_name = []


# ==================== | ESERCIZIO 1 | ====================================== #
# solo per la prima traccia lascia testo = tag...
traccia = "Emessa fattura per 250 € + 10% di IVA"
testo = tag("h3", "Esercizio") + tag("p",traccia) + testo
# ogni volta che crei un conto si aggiunge la stringa col codice a testo
conto("Crediti v/clienti", "275", "0")
conto("Iva a debito", "0", "25")
conto("Merci c/vendite", "0", "250")

# alla fine salva un file col testo
# pulsante_di_verifica()

escount = 2
def dopotesto1(testodopo1):
  ''' chiama prima dei conti per inserire la traccia dal 2ndo esercizio in poi '''
  global testo, escount

  traccia2 = testodopo1
  traccia2 = tag("p", traccia2)
  traccia2 = tag("h3", f"Esercizio {escount}") + traccia2
  escount += 1
  testo = testo + tag("p", traccia2)
  return testo


# ============= ESERCIZIO 2 ================== tutti i prossimi esercizi così
testo = dopotesto1("Ricevuto pagamento in contanti per fattura di vendita precedente")
conto("Denaro in cassa", "275", "0")
conto("Crediti v/clienti", "0", "275")
# ================ fine esercizio 2 ==========

pulsante_di_verifica()
print(testo)

# print("[hoops name='all']")
