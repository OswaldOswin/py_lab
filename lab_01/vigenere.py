def encrypt_vigenere(plaintext: str, keyword: str) -> str:


    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """

    key = []
    ciphertext = ''
    a = 0
    b = 0
    for i in range(len(keyword)):
        if ord(keyword[i]) in range (65, 91):
            key.append(ord(keyword[i]) - 65)
        if ord(keyword[i]) in range (97, 123):
            key.append(ord(keyword[i]) - 97)

    if len(key) < len(plaintext):
        key = key * int((len(plaintext) // len(key)) + 1)

    for i in range(len(plaintext)):
        if ord(plaintext[i]) in range (97, 123):
            a = ord(plaintext[i]) + key[i]
            if a in range(97, 123):
                ciphertext += chr(a)
            else:
                ciphertext += chr(a - 26)
        elif ord(plaintext[i]) in range (65, 91):
            b = ord(plaintext[i]) + key[i]
            if b in range(65, 91):
                ciphertext += chr(b)
            else:
                ciphertext += chr(b - 26)
        else:
            ciphertext += plaintext[i]
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:


    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """

    key = []
    plaintext = ''
    a = 0
    b = 0
    for i in range(len(keyword)):
        if ord(keyword[i]) in range(65, 91):
            key.append(ord(keyword[i]) - 65)
        if ord(keyword[i]) in range(97, 123):
            key.append(ord(keyword[i]) - 97)

    if len(key) < len(ciphertext):
        key = key * int((len(ciphertext) // len(key)) + 1)

    for i in range(len(ciphertext)):
        if ord(ciphertext[i]) in range(97, 123):
            a = ord(ciphertext[i]) - key[i]
            if a in range(97, 123):
                plaintext += chr(a)
            else:
                plaintext += chr(a + 26)
        elif ord(ciphertext[i]) in range(65, 91):
            b = ord(ciphertext[i]) - key[i]
            if b in range(65, 91):
                plaintext += chr(b)
            else:
                plaintext += chr(b + 26)
        else:
            plaintext += ciphertext[i]

    return plaintext