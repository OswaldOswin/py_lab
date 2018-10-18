def encrypt_caesar(plaintext: str) -> str:


    """
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """

    ciphertext = ''
    for i in range(len(plaintext)):
        if plaintext[i].isalpha():
            if ord(plaintext[i]) in range(120, 123):
                ciphertext += chr(ord(plaintext[i]) - 23)
            elif ord(plaintext[i]) in range(88, 91):
                ciphertext += chr(ord(plaintext[i]) - 23)
            else:
                ciphertext += chr(ord(plaintext[i]) + 3)
        else:
            ciphertext += plaintext[i]
    return ciphertext


print(encrypt_caesar ('PYTHON'))
print(encrypt_caesar ('python'))
print(encrypt_caesar ('Python3.6'))


def decrypt_caesar(ciphertext: str) -> str:


    """
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """

    plaintext = ''
    for i in range(len(ciphertext)):
        if ciphertext[i].isalpha():
            if ord(ciphertext[i]) in range(97, 100):
                plaintext += chr(ord(ciphertext[i]) + 23)
            elif ord(ciphertext[i]) in range(65, 68):
                plaintext += chr(ord(ciphertext[i]) + 23)
            else:
                plaintext += chr(ord(ciphertext[i]) - 3)
        else:
            plaintext += ciphertext[i]
    return plaintext


print(decrypt_caesar ('SBWKRQ'))
print(decrypt_caesar ('sbwkrq'))
print(decrypt_caesar ('Sbwkrq3.6'))
