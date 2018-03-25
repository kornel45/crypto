def get_cipher(file='20ciphers.txt'):
    ciphers_list = []
    with open(file, 'r') as f:
        for line in f:
            cipher_list = [int(x, 2) for x in line.split(' ')]
            ciphers_list.append(cipher_list)
    return ciphers_list[:-1], ciphers_list[-1]


def get_xored_ciphers(ciphers, last):
    result =[]
    for cipher in ciphers[:-1]:
        xor = []
        for i_c, i_last in zip(cipher, last):
            xor.append(i_c ^ i_last)
        result.append(xor)
    return result


def decrypt_message(ciphers, c20):
    alphanumeric = [32] + [i for i in range(65, 123) if not 91 <= i <= 96]
    xored_ciphers = get_xored_ciphers(ciphers, c20)
    result = ''
    for i, number in enumerate(c20):
        how_many_alphanumeric = []
        for letter in alphanumeric:
            how_many = 0
            for xor in xored_ciphers:
                if i < len(xor):
                    if (letter ^ xor[i]) in alphanumeric:
                        how_many += 1
            how_many_alphanumeric.append(how_many)
        index = how_many_alphanumeric.index(max(how_many_alphanumeric))
        result += chr(alphanumeric[index])
    return result


def how_many_messages(ciphers, c20):
    old = decrypt_message(ciphers[:1], c20)
    for i in range(2, 21):
        new = decrypt_message(ciphers[:i], c20)
        if new == old:
            return i-1
        old = new

original_message = """MERCUTIO Without his roe, like a dried herring: flesh, flesh, how art thou fishified! Now is he for the numbers that Petrarch flowed in. Laura to his lady was but a"""
ciphers, c20 = get_cipher()

print("Decrypted message:\n{}".format(decrypt_message(ciphers, c20)))
print('Original message:\n{}'.format(original_message))
print('It was enough to have', how_many_messages(ciphers, c20), 'messages encrypted with the same key to decrypt last one')
