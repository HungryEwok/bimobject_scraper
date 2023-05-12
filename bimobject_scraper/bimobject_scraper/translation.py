"""
Перевод на русский язык с помощью библиотеки GT
"""

from googletrans import Translator
from typing import List


translator = Translator()
lang = 'ru'


def translate_text(text: List[str]) -> List[str]:
    return translator.translate(
        text,
        dest=lang
    )
