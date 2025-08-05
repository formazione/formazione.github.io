LESSON_DATA = {
    'present_simple': {
        'title': "Present Simple",
        'course': 'Present Tenses',
        'subtitle': "Routine and Habits",
        'rules': "Used for habits and facts. Add -s/-es for he/she/it.",
        'questions': [
            {'type': 'fill_in', 'text': "Maria _______ (wake up) at 7 AM.", 'answer': 'wakes up'},
            {'type': 'fill_in', 'text': "My parents _______ (watch) TV every evening.", 'answer': 'watch'},
            {'type': 'fill_in', 'text': "He _______ (study) English at a large school.", 'answer': 'studies'},
            {'type': 'fill_in', 'text': "We _______ (not eat) meat.", 'answer': "don't eat"},
            {'type': 'fill_in', 'text': "_______ you _______ (like) pizza?", 'answer': 'Do|like'}
        ]
    },
    'present_continuous': {
        'title': "Present Continuous",
        'course': 'Present Tenses',
        'subtitle': "Actions Happening Now",
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
        'title': "Prepositions (Multiple Choice)",
        'course': 'Advanced Grammar',
        'subtitle': "Choose the correct preposition.",
        'rules': "Prepositions show relationships between nouns, pronouns, and other words.",
        'questions': [
            {'type': 'multiple_choice', 'text': "She is interested _______ art.", 'options': ['in', 'on', 'at'], 'answer': 'in'},
            {'type': 'multiple_choice', 'text': "He arrived _______ the airport.", 'options': ['in', 'on', 'at'], 'answer': 'at'},
            {'type': 'multiple_choice', 'text': "The book is _______ the table.", 'options': ['in', 'on', 'at'], 'answer': 'on'},
            {'type': 'multiple_choice', 'text': "We will meet _______ 5 PM.", 'options': ['in', 'on', 'at'], 'answer': 'at'},
            {'type': 'fill_in', 'text': "I am looking forward _______ (see) you.", 'answer': 'to seeing'}
        ]
    },
    'gerunds_infinitives': {
        'title': "Gerunds and Infinitives",
        'course': 'Advanced Grammar',
        'subtitle': "Verb Forms as Nouns",
        'rules': "Gerunds (verb-ing) and infinitives (to + verb) can act as nouns.",
        'questions': [
            {'type': 'fill_in', 'text': "I enjoy _______ (read) books.", 'answer': 'reading'},
            {'type': 'fill_in', 'text': "She decided _______ (study) medicine.", 'answer': 'to study'},
            {'type': 'fill_in', 'text': "They finished _______ (work) at 6 PM.", 'answer': 'working'},
            {'type': 'fill_in', 'text': "He wants _______ (learn) Spanish.", 'answer': 'to learn'},
            {'type': 'fill_in', 'text': "We avoid _______ (drive) in heavy traffic.", 'answer': 'driving'}
        ]
    },
    # ——— New Lessons ———
    'past_simple': {
        'title': "Simple Past",
        'course': 'Past Tenses',
        'subtitle': "Completed Actions in the Past",
        'rules': "Used for actions finished at a specific time in the past. Regular verbs add -ed; irregular verbs vary.",
        'questions': [
            {'type': 'fill_in', 'text': "They _______ (visit) the museum last weekend.", 'answer': 'visited'},
            {'type': 'fill_in', 'text': "I _______ (not see) that movie.", 'answer': "didn't see"},
            {'type': 'fill_in', 'text': "She _______ (go) to Paris in 2019.", 'answer': 'went'},
            {'type': 'fill_in', 'text': "We _______ (not play) football yesterday.", 'answer': "didn't play"},
            {'type': 'fill_in', 'text': "_______ you _______ (enjoy) the concert?", 'answer': 'Did|enjoy'}
        ]
    },
    'past_continuous': {
        'title': "Past Continuous",
        'course': 'Past Tenses',
        'subtitle': "Ongoing Actions in the Past",
        'rules': "Describes actions in progress at a certain moment in the past: was/were + verb-ing.",
        'questions': [
            {'type': 'fill_in', 'text': "He _______ (sleep) when the phone rang.", 'answer': 'was sleeping'},
            {'type': 'fill_in', 'text': "They _______ (play) cards all evening.", 'answer': 'were playing'},
            {'type': 'fill_in', 'text': "I _______ (not watch) TV at 9 PM.", 'answer': "wasn't watching"},
            {'type': 'fill_in', 'text': "It _______ (rain) when we left.", 'answer': 'was raining'},
            {'type': 'fill_in', 'text': "What _______ you _______ (do) at 7 AM?", 'answer': 'were|doing'}
        ]
    },
    'future_simple': {
        'title': "Simple Future",
        'course': 'Future Tenses',
        'subtitle': "Talking About the Future",
        'rules': "Use 'will' or 'going to' for future plans, predictions, or decisions made on the spot.",
        'questions': [
            {'type': 'fill_in', 'text': "I _______ (go) to the gym tomorrow.", 'answer': 'will go'},
            {'type': 'fill_in', 'text': "They _______ (not finish) the project by next week.", 'answer': "won't finish"},
            {'type': 'fill_in', 'text': "She _______ (visit) her aunt next month.", 'answer': 'is going to visit'},
            {'type': 'fill_in', 'text': "_______ you _______ (help) me later?", 'answer': 'Will|help'},
            {'type': 'fill_in', 'text': "We _______ (meet) at 6 PM.", 'answer': 'are going to meet'}
        ]
    },
    'modal_verbs': {
        'title': "Modal Verbs",
        'course': 'Advanced Grammar',
        'subtitle': "Ability, Permission, Obligation",
        'rules': "Modals (can, must, should, etc.) express ability, permission, obligation, advice; they don’t take -s in the third person.",
        'questions': [
            {'type': 'fill_in', 'text': "You _______ (can) swim very well.", 'answer': 'can'},
            {'type': 'fill_in', 'text': "She _______ (must) finish her homework.", 'answer': 'must'},
            {'type': 'multiple_choice', 'text': "He _______ arrive on time.", 'options': ['should', 'can', 'will'], 'answer': 'should'},
            {'type': 'fill_in', 'text': "We _______ (not have to) come if we don’t want to.", 'answer': "don't have to"},
            {'type': 'fill_in', 'text': "_______ I _______ (borrow) your pen?", 'answer': 'May|borrow'}
        ]
    },
    'passive_voice': {
        'title': "Passive Voice",
        'course': 'Advanced Grammar',
        'subtitle': "Focusing on the Action",
        'rules': "Formed with a form of 'to be' + past participle. Use 'by' to introduce the doer (optional).",
        'questions': [
            {'type': 'fill_in', 'text': "The cake _______ (make) by my mom.", 'answer': 'was made'},
            {'type': 'fill_in', 'text': "The letters _______ (deliver) every morning.", 'answer': 'are delivered'},
            {'type': 'fill_in', 'text': "The window _______ (break) yesterday.", 'answer': 'was broken'},
            {'type': 'fill_in', 'text': "This song _______ (write) by John Lennon.", 'answer': 'was written'},
            {'type': 'fill_in', 'text': "_______ the reports _______ (submit) on time?", 'answer': 'Were|submitted'}
        ]
    },
    'comparatives_superlatives': {
        'title': "Comparatives and Superlatives",
        'course': 'Advanced Grammar',
        'subtitle': "Comparing Things",
        'rules': "Use -er/-est or more/most. Short adjectives take -er/-est; longer ones take more/most.",
        'questions': [
            {'type': 'multiple_choice', 'text': "This car is _______ than that one.", 'options': ['fast', 'faster', 'fastest'], 'answer': 'faster'},
            {'type': 'multiple_choice', 'text': "She is the _______ student in the class.", 'options': ['smart', 'smarter', 'smartest'], 'answer': 'smartest'},
            {'type': 'fill_in', 'text': "My house is _______ (big) than yours.", 'answer': 'bigger'},
            {'type': 'fill_in', 'text': "This is the _______ (interesting) book I’ve read.", 'answer': 'most interesting'},
            {'type': 'fill_in', 'text': "He is _______ (good) at tennis than me.", 'answer': 'better'}
        ]
    },
    'relative_clauses': {
        'title': "Relative Clauses",
        'course': 'Advanced Grammar',
        'subtitle': "Defining and Non-defining",
        'rules': "Use who/which/that to add information about a noun. Commas separate non-defining clauses.",
        'questions': [
            {'type': 'fill_in', 'text': "The man _______ (who) helped us was kind.", 'answer': 'who helped us'},
            {'type': 'fill_in', 'text': "She bought a car _______ (that) is electric.", 'answer': 'that is electric'},
            {'type': 'fill_in', 'text': "Paris, _______ (which) is the capital of France, is beautiful.", 'answer': 'which is the capital of France'},
            {'type': 'fill_in', 'text': "Students _______ study hard get good grades.", 'answer': 'who study hard'},
            {'type': 'fill_in', 'text': "The house _______ we saw was expensive.", 'answer': 'that we saw'}
        ]
    },
    'articles': {
        'title': "Articles",
        'course': 'Advanced Grammar',
        'subtitle': "a, an, the, and zero article",
        'rules': "Use 'a' before consonant sounds, 'an' before vowel sounds; 'the' for specific nouns; no article for general plural or uncountable nouns.",
        'questions': [
            {'type': 'fill_in', 'text': "I saw ___ (a/an/the) dog in the garden.", 'answer': 'a'},
            {'type': 'fill_in', 'text': "She has ___ (a/an/the) umbrella.", 'answer': 'an'},
            {'type': 'fill_in', 'text': "___ (a/an/the) moon orbits the Earth.", 'answer': 'The'},
            {'type': 'fill_in', 'text': "Restaurants serve ___ (a/an/the) food.", 'answer': ''},
            {'type': 'fill_in', 'text': "He wants to be ___ (a/an/the) engineer.", 'answer': 'an'}
        ]
    },
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
    "Present Tenses": [k for k, v in LESSON_DATA.items() if v['course'] == 'Present Tenses'],
    "Past Tenses":   [k for k, v in LESSON_DATA.items() if v['course'] == 'Past Tenses'],
    "Future Tenses": [k for k, v in LESSON_DATA.items() if v['course'] == 'Future Tenses'],
    "Advanced Grammar": [k for k, v in LESSON_DATA.items() if v['course'] == 'Advanced Grammar'],
}

RULES_DATA = {
    'general_grammar': {
        'title': 'Fundamental Grammar Rules',
        'rules_text': [
            "The Present Simple is used for habits, routines, and general truths.",
            "For 'he', 'she', and 'it', we add -s or -es to the verb in the Present Simple.",
            "The Present Continuous is for actions that are happening at the moment of speaking.",
            "Its structure is: Subject + am/is/are + Verb-ing.",
            "A gerund is a verb ending in -ing that functions as a noun.",
            "An infinitive is the base form of a verb, usually preceded by 'to'."
        ],
        'quiz': [
            {'question': "You use Present Simple for actions happening right now.", 'answer': False},
            {'question': "You add '-s' to verbs for 'they' in Present Simple.", 'answer': False},
            {'question': "Present Continuous uses the verb 'to be' and a verb ending in '-ing'.", 'answer': True},
            {'question': "A gerund can be the subject of a sentence.", 'answer': True}
        ]
    },
    'tense_rules': {
        'title': 'Tense Usage Rules',
        'rules_text': [
            "Simple Past expresses completed actions at a specific time in the past.",
            "Regular verbs add -ed in Simple Past; irregular verbs have unique past forms.",
            "Past Continuous describes ongoing actions in the past: was/were + verb-ing.",
            "Simple Future uses 'will' or 'going to' for future intentions or predictions."
        ],
        'quiz': [
            {'question': "You use Simple Past for actions happening now.", 'answer': False},
            {'question': "Irregular verbs always end in -ed in the Simple Past.", 'answer': False},
            {'question': "Past Continuous is formed with was/were + verb-ing.", 'answer': True},
            {'question': "You can use 'going to' to talk about future plans.", 'answer': True}
        ]
    },
    'modal_rules': {
        'title': 'Modal Verbs Rules',
        'rules_text': [
            "Modals express ability (can), permission (may), obligation (must), and advice (should).",
            "Modals do not change form for subjects and have no -s in the third person.",
            "Modals are followed by the base form of the main verb without 'to' (except 'ought to').",
            "Use 'can' and 'could' for ability; 'must' for strong obligation; 'should' for suggestions."
        ],
        'quiz': [
            {'question': "Modals are followed by an -ing form of the verb.", 'answer': False},
            {'question': "You use 'must' for strong obligation.", 'answer': True},
            {'question': "Modals change form for 'he' or 'she'.", 'answer': False},
            {'question': "You can use 'may' to ask for permission.", 'answer': True}
        ]
    },
    'voice_rules': {
        'title': 'Passive Voice Rules',
        'rules_text': [
            "The passive voice focuses on the action or receiver of the action.",
            "It is formed with a form of 'to be' + past participle.",
            "The agent (doer) is introduced with 'by' (optional if unknown or irrelevant).",
            "Passive can be used in all tenses by changing the form of 'to be'."
        ],
        'quiz': [
            {'question': "Passive voice uses a form of 'to do' + past participle.", 'answer': False},
            {'question': "You can leave out the agent in a passive sentence.", 'answer': True},
            {'question': "Passive voice can be formed in any tense.", 'answer': True},
            {'question': "The structure is always 'subject + verb + object'.", 'answer': False}
        ]
    },
    'article_rules': {
        'title': 'Article Usage Rules',
        'rules_text': [
            "Use 'a' before consonant sounds and 'an' before vowel sounds.",
            "Use 'the' to refer to specific or already mentioned nouns.",
            "No article is needed for uncountable nouns when speaking generally.",
            "Use articles with singular countable nouns; plural and uncountable nouns can go without articles when general."
        ],
        'quiz': [
            {'question': "You use 'an' before words that start with consonants.", 'answer': False},
            {'question': "Use 'the' when both speaker and listener know the noun.", 'answer': True},
            {'question': "Uncountable nouns always take an article.", 'answer': False},
            {'question': "Plural countable nouns can appear without an article to speak generally.", 'answer': True}
        ]
    }
}
