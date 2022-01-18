'''
crea esercizi in partita doppia come questo:

https://aziendaitalia.altervista.org/esercizio-in-partita-doppia-sulle-vendite/


'''




def esercizio(text, dati):
  ''' creates a text with a table with the account name and the 2 sections Dare Avere '''
  global testo, sol, darecount, averecount

  # Creazione del conto in html
  traccia(text)
  for conto in dati:
    titolo, dare, avere = conto
    testo += f"""

    <!-- {titolo}   {text}  Dare: {dare} Avere: {avere} -->

    <table border=1 style="width:300">
    <td colspan=2><center>{titolo}</center><tr>
    <td  style="width:150">
  <input type="text" id="dare{darecount}" style="width:150" value=0></td><td style="width:150">
  <input type="text" id="avere{averecount}" style="width:150" value=0></td>
    </table><br><br>



  """
    sol += f"{dare} {avere} | "
    obj_input_name.append([f"dare{darecount}.value", f"avere{averecount}.value"])
    darecount +=1
    averecount +=1
  


def pulsante_di_verifica():
  ''' call this at the end of the conti(...) to see if the user inputs are right '''
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
  ''' Easy create html tags

  Example

  tag('p', 'hello')

  output

  <p>hello</p>
  '''
  return f"<{_t}>{testo}</{_t}>"


stringa = ""
darecount = 1
averecount = 1
testo = ""
sol = ""
obj_input_name = []


escount = 1
def traccia(testo_traccia):
  ''' prints the text to make the exercise, call this before conti(...) '''
  global testo, escount
  testo_puro = testo
  tracc = tag("p", testo_traccia)
  tracc = tag("h3", f"Esercizio {escount}") + tracc
  escount += 1
  testo = testo + tag("p", tracc)
  
  

# ==================== | ESERCIZIO 1 | ====================================== #
esercizio("Emessa fattura per 250 € + 10% di IVA",(
  ("Crediti v/clienti", "275", "0"),
  ("Iva a debito", "0", "25"),
  ("Merci c/vendite", "0", "250")))


# ============= ESERCIZIO 2 ================== tutti i prossimi esercizi così
esercizio("Ricevuto pagamento in contanti per fattura di vendita precedente",(
  ("Denaro in cassa", "275", "0"),
  ("Crediti v/clienti", "0", "275")))


# Pulsante finale di verifica
pulsante_di_verifica()

# Copia questo testo in un file html
print(testo)

# This is for the blog
# print("[hoops name='all']")
