from googletrans import Translator

def translate(phrase, language):

    translator = Translator()

    out = translator.translate(phrase, dest=language)

    return out.text

