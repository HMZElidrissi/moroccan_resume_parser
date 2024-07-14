from nltk.corpus import stopwords

NAME_PATTERN = [
    {'POS': 'PROPN'},
    {'POS': 'PROPN', 'OP': '?'},
    {'POS': 'PROPN', 'OP': '?'}
]

EDUCATION = [
    'Bac', 'Baccalauréat', 'Licence', 'Master', 'Doctorat', 'LST',
    'Diplôme d\'ingénieur', 'Bachelor', 'PhD', 'Ingénieur', 'DEUG', 'DUT', 'BTS',
    'Ingénieur d\'état', 'DEUST', 'M1', 'M2', 'ENSA', 'EST', 'ENCG', 'FST', 'FSJES',
    'Classe Préparatoire', 'Grande École', 'École d\'Ingénieurs'
]

JOB_TITLE = [
    "Développeur", "Ingénieur", "Consultant", "Chef de Projet", "Analyste",
    "Gestionnaire", "Responsable", "Directeur", "Technicien", "Commercial",
    "Stagiaire", "PFE", "PFA", "Stage", "Intern"
]

EXPERIENCE = [
    "Expérience Professionnelle", "Projets", "Experience", "Expériences Professionnelles",
    "Professional Experience", "Stages", "Internship", "PFE", "PFA", "Projet de Fin d'Études"
]

NOT_ALPHA_NUMERIC = r'[^a-zA-Z\d]'
NUMBER = r'\d+'

MONTHS_SHORT = r'''(jan|fév|mar|avr|mai|juin|juil|aoû|sep|oct|nov|déc)'''
MONTHS_LONG = r'''(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)'''
MONTH = r'(' + MONTHS_SHORT + r'|' + MONTHS_LONG + r')'
YEAR = r'(((20|19)(\d{2})))'

STOPWORDS = set(stopwords.words('french'))

RESUME_SECTIONS = [
    'compétences', 'expérience', 'éducation', 'formation', 'projets',
    'expérience professionnelle', 'publications', 'certifications',
    'langues', 'centres d\'intérêt', 'loisirs', 'références'
]

COMPETENCIES = {
    'teamwork': [
        'collaborer', 'équipe', 'coopérer', 'coordonner', 'contribuer'
    ],
    'communication': [
        'communiquer', 'présenter', 'négocier', 'rédiger', 'exposer'
    ],
    'leadership': [
        'diriger', 'gérer', 'superviser', 'manager', 'motiver', 'guider'
    ],
    'problem_solving': [
        'résoudre', 'analyser', 'optimiser', 'concevoir', 'développer'
    ]
}

MEASURABLE_RESULTS = {
    'metrics': [
        'augmenté', 'réduit', 'amélioré', '%', 'pourcent', 'dirhams', 'dh', 'MAD',
        'millions', 'milliers', 'économisé', 'généré', 'croissance', 'chiffre d\'affaires'
    ],
    'action_words': [
        'développé', 'mis en place', 'créé', 'lancé', 'implémenté', 'géré',
        'dirigé', 'coordonné', 'formé', 'négocié', 'obtenu', 'réalisé'
    ]
}