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

    <table border=0>
    <td width='300'><center>{titolo}</center>
    <td>


    <!-- BUTTON SI -->

  <input type="button" id="dare{darecount}" style="width:150" value='SI' onclick="if(this.value=='{dare}'){{risdare{darecount}.value=this.value;risavere{averecount}.value='0';this.style.background='yellow';avere{averecount}.style.background=''}}else{{this.style.background='yellow';avere{averecount}.style.background=''}}"></td><td style="width:150">



  <input type="button" id="avere{averecount}" style="width:150" value='NO' onclick="if(this.value=='{avere}'){{risdare{darecount}.value='0';risavere{averecount}.value=this.value;this.style.background='yellow';dare{darecount}.style.background=''}}else{{this.style.background='yellow';dare{darecount}.style.background=''}}"></td>


  <input type="hidden" id="risdare{averecount}" style="width:150" value=''> <input type="hidden" id="risavere{averecount}" style="width:150" value=''></td>
    </table>
<hr>


  """
    sol += f"{dare} {avere}"
    # unisce le risposte per confronto con sol

    risp = f"risdare{darecount}.value + ' ' + risavere{averecount}.value + "
    obj_input_name.append(risp)
    print(obj_input_name)
    darecount +=1
    averecount +=1
  


def pulsante_di_verifica():
  ''' call this at the end of the conti(...) to see if the user inputs are right '''
  global testo, stringa

  
  stringa = ""
  # Unisce le risposte da confrontare con sol
  # for risp in obj_input_name:
  #   stringa += risp
  stringa = "".join(obj_input_name)
  stringa = stringa[:-2]
  print(stringa)
  # stringa = stringa[:-6]
  # stringa = stringa + "|'"
  # # stringa += "'|'"


  # inp1 serve per quizlive soltanto
  testo += f"""

<!-- ############### VERIFY INPUT ################ -->

  <button onclick="if ({stringa}=='{sol}'){{ver1.value='giusto'}}else{{ver1.value='sbagliato'}};console.log({stringa});console.log('{sol}');inp1.value={stringa}+' '+ver1.value";>Verifica risposte</button><input id='ver1' type='text'>"""
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
  tracc = tag("h3", f"Vero o Falso parte {escount}") + tracc
  escount += 1
  testo = testo + tag("p", tracc)
  
  

# ==================== | ESERCIZIO 1 | ====================================== #
esercizio("Il marketing mix",(

  # Affermazioni vero o false

  ("Il marketing mix fa parte del Marketing operativo", "SI", "0"),
  ("Place sta per distribuzione", "SI", "0"),
  ("COMUNICAZIONE si traduce con Comunication", "0", "NO"))


)





# Pulsante finale di verifica
pulsante_di_verifica()

# Copia questo testo in un file html
print(testo)

# This is for the blog
# print("[hoops name='all']")
