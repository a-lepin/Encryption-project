import encryption

class СaesarСipherСracker():
    def __init__(self, language: str):
        """Allows you to use СaesarСipherСracker with basic languages.

        Automatically supporting:
        - English 'eng',
        - Russian 'rus'.

        Throws ValueError if language is not supporting. 
        """

        self._language = language

    def crack_caesar(self, ciphertext: str) -> str:
        """Finds the intended key of caesar cipher and returns decrypted text with this key.
        
        This function uses frequency analysis method.
        The function goes through all the shift options and finds the most suitable one.
        """

        qualities = list()
        for shift in range(0, len(self._alphabets[self._language])):
            encr = encryption.Encryption(self._language)
            shifted_ciphertext = encr.encrypt_caesar(ciphertext, shift)
            quality = self._calculate_deviation_from_distribution(shifted_ciphertext)
            qualities.append(quality)
        
        shift = qualities.index(min(qualities))
        return encr.encrypt_caesar(ciphertext, shift)

    def _calculate_deviation_from_distribution(self, text: str) -> float:
        """Returns the squared deviation text's letters from the distribution."""

        counts = dict()
        frequncy = self._letter_frequency_in_alphabets[self._language]
        for letter in frequncy.keys():
            counts[letter] = 0
        letter_count = 0
        for letter in text.lower():
            if letter in self._alphabets[self._language]:
                counts[letter] += 1
                letter_count += 1
        if letter_count != 0:
            for char_count in counts.values():
                char_count /= letter_count
        
        deviation: float = 0
        for letter in frequncy.keys():
            deviation += (counts[letter] - frequncy[letter])**2
        return deviation

    _letter_frequency_in_alphabets: dict[str, dict[str, float]] = {
        # source: https://ru.wikipedia.org/wiki/%D0%A7%D0%B0%D1%81%D1%82%D0%BE%D1%82%D0%BD%D0%BE%D1%81%D1%82%D1%8C
        'rus': {
            'а': 08.01, 'б': 01.59, 'в': 04.54, 'г': 01.70, 'д': 02.98, 'е': 08.45, 'ё': 00.04,
            'ж': 00.94, 'з': 01.65, 'и': 07.35, 'й': 01.21, 'к': 03.49, 'л': 04.40, 'м': 03.21,
            'н': 06.70, 'о': 10.97, 'п': 02.81, 'р': 04.73, 'с': 05.47, 'т': 06.26, 'у': 02.62,
            'ф': 00.26, 'х': 00.97, 'ц': 00.48, 'ч': 01.44, 'ш': 00.73, 'щ': 00.36, 'ъ': 00.04,
            'ы': 01.90, 'ь': 01.74, 'э': 00.32, 'ю': 00.64, 'я': 02.01
        },
        # source: https://ru.wikipedia.org/wiki/%D0%90%D0%BD%D0%B3%D0%BB%D0%B8%D0%B9%D1%81%D0%BA%D0%B8%D0%B9_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82
        'eng': {
            'a': 08.17, 'b': 01.49, 'c': 02.78, 'd': 04.25, 'e': 12.70, 'f': 02.23, 'g': 02.02,
            'h': 06.09, 'i': 06.97, 'j': 00.15, 'k': 00.77, 'l': 04.03, 'm': 02.41, 'n': 06.75,
            'o': 07.51, 'p': 01.93, 'q': 00.01, 'r': 05.99, 's': 06.33, 't': 09.06, 'u': 02.76,
            'v': 00.98, 'w': 02.36, 'x': 00.15, 'y': 01.97, 'z': 00.07
        }
    }

    _alphabets: dict[str, str] = {'rus': 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя',
                                  'eng': 'abcdefghijklmnopqrstuvwxyz'}

    _language: str