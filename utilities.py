import string
import regex as re
from translate import Translator
from wordlist import levelOne, levelTwo, levelThree

# Constants
LANGUAGE_CODES = ['fr', 'it', 'es', 'ru', 'pt', 'zh', 'de']
LANGUAGES = ['French', 'Italian', 'Spanish', 'Russian', 'Portuguese', 'Chinese', 'German']
LEVELS = [levelOne, levelTwo, levelThree]
SIMILARITY_THRESHOLD = 70

def translate(text, from_lang, to_lang):
    try:
        translator = Translator(provider='mymemory', from_lang=from_lang, to_lang=to_lang)
        translation = translator.translate(text)
        translation = translation.translate(str.maketrans('', '', string.punctuation))
        translation = re.sub(r'[^\p{L} ]+', '', translation).lower()
        return translation
    except Exception as e:
        print(f"Translation failed: {e}")
        return ""
