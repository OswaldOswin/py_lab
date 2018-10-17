def encrypt_caesar (plaintext: str, shift: int):
    ciphertext = ''
    for i in range(len(plaintext)):
        if plaintext[i].isalpha():
            if ord(plaintext[i]) in range((123 - shift), 123):
                ciphertext += chr(ord(plaintext[i]) - (26 - shift))
            elif ord(plaintext[i]) in range((91 - shift), 91):
                ciphertext += chr(ord(plaintext[i]) - (26 - shift))
            else:
                ciphertext += chr(ord(plaintext[i]) + shift)
        else:
            ciphertext += plaintext[i]
    return ciphertext
print(encrypt_caesar ('PYTHON', 3))
print(encrypt_caesar ('python', 3))
print(encrypt_caesar ('Python3.6', 3))

def decrypt_caesar (ciphertext: str, shift: int):
    plaintext = ''
    for i in range(len(ciphertext)):
        if ciphertext[i].isalpha():
            if ord(ciphertext[i]) in range(97, (97 + shift)):
                plaintext += chr(ord(ciphertext[i]) + (26 - shift))
            elif ord(ciphertext[i]) in range(65, (65 + shift)):
                plaintext += chr(ord(ciphertext[i]) + (26 - shift))
            else:
                plaintext += chr(ord(ciphertext[i]) - shift)
        else:
            plaintext += ciphertext[i]
    return plaintext
print(decrypt_caesar ('SBWKRQ', 3))
print(decrypt_caesar ('sbwkrq', 3))
print(decrypt_caesar ('Sbwkrq3.6', 3))
