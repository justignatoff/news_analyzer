import pymorphy2

morph = pymorphy2.MorphAnalyzer()


def text_cleaner(text):
    # к нижнему регистру
    text = text.lower()

    # оставляем в предложении только русские буквы (таким образом
    # удалим и ссылки, и имена пользователей, и пунктуацию и т.д.)
    alph = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

    cleaned_text = ''
    for char in text:
        if (char.isalpha() and char[0] in alph) or (char == ' '):
            cleaned_text += char

    result = []
    for word in cleaned_text.split():
        # лемматизируем
        result.append(morph.parse(word)[0].normal_form)

    return ' '.join(result)
