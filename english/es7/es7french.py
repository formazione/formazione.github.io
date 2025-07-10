import random
import pyttsx3
import platform
import os

# --- INIZIALIZZAZIONE ---

# Lista di frasi in francese per l'esercizio
master_sentence_list = [
    "Le soleil est chaud", "Mon chien est grand", "Je peux courir vite", "Elle a une voiture rouge", "Nous aimons jouer",
    "Il est mon ami", "Le chat est petit", "Je vois un oiseau", "Ceci est un livre", "J'ai un stylo",
    "Le ciel est bleu", "J'aime ma maman", "Il peut sauter haut", "La balle est ronde", "Nous mangeons du poisson",
    "Elle chante bien", "L'arbre est grand", "Je bois du lait", "Il a un vélo bleu", "Je m'appelle Tom",
    "Je vais à l'école", "L'herbe est verte", "J'ai deux mains", "Elle aime lire", "Nous jouons à un jeu",
    "Le cochon est rose", "Je peux voir la lune", "Il frappe le ballon", "Le canard peut nager", "Je suis assis sur une chaise",
    "Le poisson est dans la mer", "Je porte un chapeau bleu", "C'est un bon garçon", "Elle mange une pomme", "Nous aimons apprendre",
    "La grenouille est verte", "J'ai un nouveau jouet", "Il monte à cheval", "La vache fait meuh", "Je peux écrire mon nom",
    "L'oiseau peut voler", "Je vois avec mes yeux", "Il joue du tambour", "Elle dessine une fleur", "Nous allons au parc",
    "L'ours est brun", "J'aime manger du gâteau", "Il lit une histoire", "Elle a les cheveux longs", "Nous sommes une famille heureuse"
]

# Inizializza il motore di sintesi vocale (text-to-speech)
try:
    engine = pyttsx3.init()
except ImportError:
    print("Erreur : La bibliothèque 'pyttsx3' n'est pas installée.")
    print("Veuillez l'installer en exécutant : pip install pyttsx3")
    exit()
except RuntimeError:
    print("Erreur : Aucun pilote de synthèse vocale trouvé.")
    print("Il peut être nécessaire d'installer 'espeak' sur Linux.")
    exit()

# Imposta la voce in francese
voices = engine.getProperty('voices')
french_voice_id = None
for voice in voices:
    # Cerca una voce con il codice lingua 'fr'
    if hasattr(voice, 'languages') and voice.languages:
        if any('fr' in lang.lower() for lang in voice.languages):
            french_voice_id = voice.id
            break
    # Fallback: cerca 'French' nel nome della voce
    if hasattr(voice, 'name') and 'french' in voice.name.lower():
        french_voice_id = voice.id
        break

if french_voice_id:
    engine.setProperty('voice', french_voice_id)
else:
    print("\nAvertissement : Aucune voix française n'a été trouvée. La voix par défaut sera utilisée.")


engine.setProperty('rate', 140) # Imposta una velocità di lettura più lenta

# --- FUNZIONI PRINCIPALI ---

def speak_sentence(sentence):
    """
    Usa il motore di sintesi vocale per leggere una frase.
    """
    print("\nÉcoutez attentivement...")
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

    print("--- Nouvel exercice d'écoute ! ---")
    print("Écrivez la phrase que vous entendez. Appuyez sur Entrée pour confirmer.")

    # Itera su ogni frase selezionata
    for i, sentence in enumerate(current_sentences):
        print("-" * 30)
        print(f"Phrase {i + 1} sur {len(current_sentences)}")
        
        # Leggi la frase
        speak_sentence(sentence)
        
        # Chiedi all'utente di scrivere la frase
        user_input = input("Écrivez la phrase ici : ")
        
        # Confronta la risposta (ignorando maiuscole/minuscole e spazi extra)
        if user_input.strip().lower() == sentence.lower():
            print("✅ Correct ! Excellent travail.")
            correct_answers += 1
        else:
            print(f"❌ Pas tout à fait. La phrase correcte était : '{sentence}'")
            
    # Mostra il punteggio finale
    print("\n--- Exercice terminé ! ---")
    print(f"Votre score : {correct_answers} / {len(current_sentences)}")
    print("-" * 30)


# --- ESECUZIONE DEL PROGRAMMA ---

if __name__ == "__main__":
    clear_screen()
    print("Bienvenue dans l'exercice d'écoute en Python !")
    
    while True:
        start_new_exercise()
        
        # Chiedi all'utente se vuole giocare di nuovo
        play_again = input("\nVoulez-vous faire un autre exercice ? (o/n) : ").lower()
        if play_again != 'o':
            print("Merci d'avoir joué ! À bientôt.")
            break
        clear_screen()
