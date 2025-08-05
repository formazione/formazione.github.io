# morelessons.py

# ===================================================================================
# LESSON & RULES DATA
# ===================================================================================

# NOTE: All 'questions' are now a list of dictionaries to support different question types.
LESSON_DATA = {
    'present_simple': {
        'title': "Present Simple", 'course': 'Present Tenses', 'subtitle': "Routine and Habits",
        'rules': "Used for habits and facts. Add -s/-es for he/she/it.",
        'questions': [
            {'type': 'fill_in', 'text': "Maria _______ (wake up) at 7 AM.", 'answer': 'wakes up'},
            {'type': 'fill_in', 'text': "My parents _______ (watch) TV every evening.", 'answer': 'watch'},
            {'type': 'fill_in', 'text': "He _______ (study) English at a large school.", 'answer': 'studies'},
            {'type': 'fill_in', 'text': "We _______ (not, eat) meat.", 'answer': "don't eat"},
            {'type': 'fill_in', 'text': "_______ you _______ (like) pizza?", 'answer': 'Do|like'} # Pipe for multiple blanks
        ]
    },
    'present_continuous': {
        'title': "Present Continuous", 'course': 'Present Tenses', 'subtitle': "Actions Happening Now",
        'rules': "Used for actions happening right now. Form: am/is/are + verb-ing.",
        'questions': [
            {'type': 'fill_in', 'text': "A boy _______ (eat) an apple.", 'answer': 'is eating'},
            {'type': 'fill_in', 'text': "A girl _______ (run) in the park.", 'answer': 'is running'},
            {'type': 'fill_in', 'text': "Two friends _______ (talk).", 'answer': 'are talking'},
            {'type': 'fill_in', 'text': "A dog _______ (sleep) on the sofa.", 'answer': 'is sleeping'},
            {'type': 'fill_in', 'text': "A mother _______ (cook) dinner.", 'answer': 'is cooking'}
        ]
    },
    'prepositions_choice': {
        'title': "Prepositions (Multiple Choice)", 'course': 'Advanced Grammar', 'subtitle': "Choose the correct preposition.",
        'rules': "Prepositions show relationships between nouns, pronouns, and other words.",
        'questions': [
            {'type': 'multiple_choice', 'text': "She is interested _______ art.", 'options': ['in', 'on', 'at'], 'answer': 'in'},
            {'type': 'multiple_choice', 'text': "He arrived _______ the airport.", 'options': ['in', 'on', 'at'], 'answer': 'at'},
            {'type': 'multiple_choice', 'text': "The book is _______ the table.", 'options': ['in', 'on', 'at'], 'answer': 'on'},
            {'type': 'multiple_choice', 'text': "We will meet _______ 5 PM.", 'options': ['in', 'on', 'at'], 'answer': 'at'},
            {'type': 'fill_in', 'text': "I am looking forward _______ (see) you.", 'answer': 'to seeing'} # Mixed type for variety
        ]
    },
    'gerunds_infinitives': {
        'title': "Gerunds and Infinitives", 'course': 'Advanced Grammar', 'subtitle': "Verb Forms as Nouns",
        'rules': "Gerunds (verb-ing) and infinitives (to + verb) can act as nouns.",
        'questions': [
            {'type': 'fill_in', 'text': "I enjoy _______ (read) books.", 'answer': 'reading'},
            {'type': 'fill_in', 'text': "She decided _______ (study) medicine.", 'answer': 'to study'},
            {'type': 'fill_in', 'text': "They finished _______ (work) at 6 PM.", 'answer': 'working'},
            {'type': 'fill_in', 'text': "He wants _______ (learn) Spanish.", 'answer': 'to learn'},
            {'type': 'fill_in', 'text': "We avoid _______ (drive) in heavy traffic.", 'answer': 'driving'}
        ]
    },
    'reading_comprehension_1': {
        'title': "Reading: A Day at the Beach",
        'course': 'Reading Skills',
        'subtitle': "Fill in the blanks using the word bank.",
        'type': 'word_bank', # New lesson type
        'word_bank': ['sunny', 'sandcastles', 'waves', 'picnic', 'seagulls', 'cool'],
        'text': "It was a beautiful, _______ day, so we decided to go to the beach. We built huge _______ near the water. The sound of the crashing _______ was very relaxing. For lunch, we had a lovely _______ with sandwiches and fruit. The _______ were flying overhead, hoping for a snack. The water was _______ and refreshing when we went for a swim.",
        'answers': ['sunny', 'sandcastles', 'waves', 'picnic', 'seagulls', 'cool']
    }
}

COURSES = {
    "All Topics": list(LESSON_DATA.keys()),
    "Present Tenses": [k for k, v in LESSON_DATA.items() if v.get('course') == 'Present Tenses'],
    "Advanced Grammar": [k for k, v in LESSON_DATA.items() if v.get('course') == 'Advanced Grammar'],
    "Reading Skills": [k for k, v in LESSON_DATA.items() if v.get('course') == 'Reading Skills'],
}
