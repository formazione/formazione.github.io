import random
import pyttsx3
import platform
import os

# --- INIZIALIZZAZIONE ---

# Lista di frasi per l'esercizio
master_sentence_list = [
    "The sun is hot", "My dog is big", "I can run fast", "She has a red car", "We like to play",
    "He is my friend", "The cat is small", "I see a bird", "This is a book", "I have a pen",
    "The sky is blue", "I love my mom", "He can jump high", "The ball is round", "We eat fish",
    "She can sing well", "The tree is tall", "I drink milk", "He has a blue bike", "My name is Tom",
    "I go to school", "The grass is green", "I have two hands", "She likes to read", "We play a game",
    "The pig is pink", "I can see the moon", "He kicks the ball", "The duck can swim", "I sit on a chair",
    "The fish is in the sea", "I wear a blue hat", "He is a good boy", "She eats an apple", "We love to learn",
    "The frog is green", "I have a new toy", "He can ride a horse", "The cow says moo", "I can write my name",
    "The bird can fly", "I see with my eyes", "He plays the drum", "She draws a flower", "We go to the park",
    "The bear is brown", "I like to eat cake", "He reads a story", "She has long hair", "We are a happy family"
]

# Inizializza il motore di sintesi vocale (text-to-speech)
try:
    engine = pyttsx3.init()
except ImportError:
    print("Errore: La libreria 'pyttsx3' non è installata.")
    print("Per favore, installala eseguendo: pip install pyttsx3")
    exit()
except RuntimeError:
    print("Errore: Nessun driver per la sintesi vocale trovato.")
    print("Potrebbe essere necessario installare 'espeak' su Linux o 'nsss' su Mac.")
    exit()

# Imposta la voce in inglese
voices = engine.getProperty('voices')
english_voice_id = None
for voice in voices:
    if 'en_US' in voice.languages or 'English' in voice.name:
        english_voice_id = voice.id
        break
if english_voice_id:
    engine.setProperty('voice', english_voice_id)

engine.setProperty('rate', 140) # Imposta una velocità di lettura più lenta

# --- FUNZIONI PRINCIPALI ---

def speak_sentence(sentence):
    """
    Usa il motore di sintesi vocale per leggere una frase.
    """
    print("\nAscolta attentamente...")
    engine.say(sentence)
    engine.runAndWait()

def clear_screen():
    """
    Pulisce lo schermo della console per una migliore leggibilità.
    """
    # Per Windows
    if platform.system() == "Windows":
        os.system('cls')
    # Per Mac e Linux
    else:
        os.system('clear')

def start_new_exercise():
    """
    Logica principale per un singolo esercizio.
    """
    # Seleziona 5 frasi casuali dalla lista principale
    current_sentences = random.sample(master_sentence_list, 5)
    correct_answers = 0

    print("--- Inizia un nuovo esercizio di ascolto! ---")
    print("Scrivi la frase che senti. Premi Invio per confermare.")

    # Itera su ogni frase selezionata
    for i, sentence in enumerate(current_sentences):
        print("-" * 30)
        print(f"Frase {i + 1} di {len(current_sentences)}")
        
        # Leggi la frase
        speak_sentence(sentence)
        
        # Chiedi all'utente di scrivere la frase
        user_input = input("Scrivi la frase qui: ")
        
        # Confronta la risposta (ignorando maiuscole/minuscole e spazi extra)
        if user_input.strip().lower() == sentence.lower():
            print("✅ Corretto! Ottimo lavoro.")
            correct_answers += 1
        else:
            print(f"❌ Non proprio. La frase corretta era: '{sentence}'")
            
    # Mostra il punteggio finale
    print("\n--- Esercizio Completato! ---")
    print(f"Il tuo punteggio: {correct_answers} / {len(current_sentences)}")
    print("-" * 30)


# --- ESECUZIONE DEL PROGRAMMA ---

if __name__ == "__main__":
    clear_screen()
    print("Benvenuto nell'esercizio di ascolto in Python!")
    
    while True:
        start_new_exercise()
        
        # Chiedi all'utente se vuole giocare di nuovo
        play_again = input("\nVuoi fare un altro esercizio? (s/n): ").lower()
        if play_again != 's':
            print("Grazie per aver giocato! A presto.")
            break
        clear_screen()
