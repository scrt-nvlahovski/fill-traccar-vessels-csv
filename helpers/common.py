def transliterate_bulgarian_to_english(text):
    # Транслитерационна таблица за български букви
    transliteration_table = {
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ж': 'Zh', 'З': 'Z',
        'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P',
        'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H', 'Ц': 'Ts', 'Ч': 'Ch',
        'Ш': 'Sh', 'Щ': 'Sht', 'Ъ': 'A', 'Ь': 'Y', 'Ю': 'YU', 'Я': 'Ya',
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ж': 'zh', 'з': 'z',
        'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
        'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch',
        'ш': 'sh', 'щ': 'sht', 'ъ': 'a', 'ь': 'y', 'ю': 'yu', 'я': 'ya'
    }

    # Транслитерация на текста
    result = []
    for char in text:
        if char in transliteration_table:
            result.append(transliteration_table[char])
        else:
            result.append(char)

    return ''.join(result)


def validate_phone_number(phone_number):
    digits_only = ''.join(filter(str.isdigit, phone_number)).lstrip('0')

    if digits_only.startswith('359') and len(digits_only) > 9:
        digits_only = '0' + digits_only[3:]
    if len(digits_only) == 10 and digits_only.startswith('0'):
        return digits_only
    elif digits_only.startswith('00359') and len(digits_only) > 10:
        return '0' + digits_only[2:11]
    elif len(digits_only) == 9 and not digits_only.startswith('0'):
        return '0' + digits_only
    elif len(digits_only) < 10:
        return None
    elif len(digits_only) > 10:
        return None
    else:
        return None
