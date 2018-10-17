def encode_vigener (word, keyword):
    key = []
    newword = ''
    a = 0
    b = 0
    for i in range(len(keyword)):
        if ord(keyword[i]) in range (65, 91):
            key.append(ord(keyword[i]) - 65)
        if ord(keyword[i]) in range (97, 123):
            key.append(ord(keyword[i]) - 97)

    if len(key) < len(word):
        key = key * int((len(word) // len(key)) + 1)

    for i in range(len(word)):
        if ord(word[i]) in range (97, 123):
            a = ord(word[i]) + key[i]
            if a in range(97, 123):
                newword += chr(a)
            else:
                newword += chr(a - 26)
        elif ord(word[i]) in range (65, 91):
            b = ord(word[i]) + key[i]
            if b in range(65, 91):
                newword += chr(b)
            else:
                newword += chr(b - 26)
        else:
            newword += word[i]

    return(newword)
print(encode_vigener('ATTACKATDAWN', 'LEMONLEMONLE'))

def decode_vigener (word, keyword):
    key = []
    newword = ''
    a = 0
    b = 0
    for i in range(len(keyword)):
        if ord(keyword[i]) in range (65, 91):
            key.append(ord(keyword[i]) - 65)
        if ord(keyword[i]) in range (97, 123):
            key.append(ord(keyword[i]) - 97)

    if len(key) < len(word):
        key = key * int((len(word) // len(key)) + 1)

    for i in range(len(word)):
        if ord(word[i]) in range (97, 123):
            a = ord(word[i]) - key[i]
            if a in range(97, 123):
                newword += chr(a)
            else:
                newword += chr(a + 26)
        elif ord(word[i]) in range (65, 91):
            b = ord(word[i]) - key[i]
            if b in range(65, 91):
                newword += chr(b)
            else:
                newword += chr(b + 26)
        else:
            newword += word[i]

    return(newword)
print(decode_vigener('LXFOPVEFRNHR', 'LEMONLEMONLE'))



