custom_analyzer = {
    'type': 'custom',
    'tokenizer': 'standard',
    'char_filter': ['punctuation_marks'],
    'filter': ['lowercase', 'stop']
}

char_filter_punctuation_marks = {
        'punctuation_marks': {
            'type': 'pattern_replace',
            'pattern': '[\\p{P}-[.]]',
            'replacement': ''
        }
}

analysis_settings = {
            'tokenizer': {
                'standard': {
                    'type': 'standard'
                }
            },
            'char_filter': {
                'replace_dash': char_filter_punctuation_marks  # Если нужно настраивать символы, например, дефисы
            },
            'filter': {
                'lowercase': {'type': 'lowercase'},

                # Стоп-слова для разных языков
                'stop': {
                    'type': 'stop',
                    'stopwords': {
                        'russian': '_russian_',  # Стоп-слова для русского языка
                        'armenian': '_armenian_',  # Стоп-слова для армянского языка
                        'belarusian': '_belarusian_',  # Стоп-слова для белорусского языка
                        'kazakh': '_kazakh_',  # Стоп-слова для казахского языка
                        'kyrgyz': '_kyrgyz_',  # Стоп-слова для кыргызского языка
                        'moldavian': '_moldavian_',  # Стоп-слова для молдавского (румынский)
                        'tajik': '_tajik_',  # Стоп-слова для таджикского языка
                        'turkmen': '_turkmen_',  # Стоп-слова для туркменского языка
                        'uzbek': '_uzbek_',  # Стоп-слова для узбекского языка
                        'english': '_english_'  # Стоп-слова для английского языка
                    }
                },

                # Стеммеры для разных языков
                'russian_stemmer': {'type': 'stemmer', 'stopwords': '_russian_'},  # Стеммер для русского
                'armenian_stemmer': {'type': 'stemmer', 'stopwords': '_armenian_'},  # Стеммер для армянского
                'belarusian_stemmer': {'type': 'stemmer', 'stopwords': '_belarusian_'},  # Стеммер для белорусского
                'kazakh_stemmer': {'type': 'stemmer', 'stopwords': '_kazakh_'},  # Стеммер для казахского
                'kyrgyz_stemmer': {'type': 'stemmer', 'stopwords': '_kyrgyz_'},  # Стеммер для кыргызского
                'moldavian_stemmer': {'type': 'stemmer', 'stopwords': '_moldavian_'},
                # Стеммер для молдавского (румынский)
                'tajik_stemmer': {'type': 'stemmer', 'stopwords': '_tajik_'},  # Стеммер для таджикского
                'turkmen_stemmer': {'type': 'stemmer', 'stopwords': '_turkmen_'},  # Стеммер для туркменского
                'uzbek_stemmer': {'type': 'stemmer', 'stopwords': '_uzbek_'},  # Стеммер для узбекского
                'english_stemmer': {'type': 'stemmer', 'stopwords': '_english_'}  # Стеммер для английского
            },
            'analyzer': {
                'custom_analyzer': {
                    'type': 'custom',
                    'tokenizer': 'standard',  # Используем стандартный токенизатор
                    'char_filter': ['replace_dash'],  # Применяем фильтры символов, если нужно
                    'filter': [
                        'lowercase',  # Применяем преобразование в нижний регистр
                        'stop',  # Применяем фильтр стоп-слов для разных языков
                        'russian_stemmer', 'armenian_stemmer', 'belarusian_stemmer',
                        'kazakh_stemmer', 'kyrgyz_stemmer', 'moldavian_stemmer',
                        'tajik_stemmer', 'turkmen_stemmer', 'uzbek_stemmer', 'english_stemmer'
                    ]
                }
            }
        }

