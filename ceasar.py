def encode_ceasar (a):
    b = ''
    for i in range(len(a)):
        if a[i].isalpha():
            if ord(a[i]) in range(120, 123):
                b += chr(ord(a[i]) - 23)
            elif ord(a[i]) in range(88, 91):
                b += chr(ord(a[i]) - 23)
            else:
                b += chr(ord(a[i]) + 3)
        else:
            b += a[i]
    return(b)

print(encode_ceasar('AbYz12'))

def decode_ceasar (a):
    b = ''
    for i in range(len(a)):
        if a[i].isalpha():
            if ord(a[i]) in range(97, 100):
                b += chr(ord(a[i]) + 23)
            elif ord(a[i]) in range(65, 68):
                b += chr(ord(a[i]) + 23)
            else:
                b += chr(ord(a[i]) - 3)
        else:
            b += a[i]
    return(b)
print(decode_ceasar('DeBc12'))