# Copyright 2019, Leejae Karinja, All rights reserved.

import numpy

def decrypt(key, ciphertext):
    assert(is2by2(key));

    inv = inverse(key)

    ciphertext = [ord(letter) - 65 for letter in ciphertext]
    pairs = zip(list(ciphertext)[::2], list(ciphertext)[1::2])

    decrypted = ''

    for pair in pairs:
        decrypted += ''.join([chr((val % 26) + 65) for val in numpy.dot(inv, pair)])

    print decrypted
    return decrypted

def crack(start_plain, ciphertext):
    assert(len(start_plain) == 4)

    start_plain = [ord(letter) - 65 for letter in start_plain]
    start_cipher = [ord(letter) - 65 for letter in list(ciphertext)[:4]]

    inv = inverse([[start_plain[0], start_plain[2]], [start_plain[1], start_plain[3]]])
    key = numpy.dot([[start_cipher[0], start_cipher[2]], [start_cipher[1], start_cipher[3]]], inv)

    for x, row in enumerate(key):
        for y, element in enumerate(row):
            key[x][y] = key[x][y] % 26

    print 'Key:\n%s' % key
    return decrypt(key, ciphertext)

def inverse(matrix):
    assert(is2by2(matrix))

    inverses = {1:1, 3:9, 5:21, 7:15, 9:3, 11:19, 15:7, 17:23, 19:11, 21:5, 23:17, 25:25}

    det = inverses[int((matrix[0][0] * matrix[1][1]) - (matrix[0][1] * matrix[1][0])) % 26]
    inv = [[matrix[1][1], -1 * matrix[0][1]], [-1 * matrix[1][0], matrix[0][0]]]

    for x, row in enumerate(inv):
        for y, element in enumerate(row):
            inv[x][y] = (det * inv[x][y]) % 26

    return inv

def is2by2(matrix):
    if len(matrix) == 2:
        return all (len(row) == 2 for row in matrix)
    return false
