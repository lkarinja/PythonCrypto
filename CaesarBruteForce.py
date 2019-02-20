def caesar(ciphertext):
  for x in range(0, 26):
    plaintext = list()
    for letter in ciphertext:
      plaintext.append(chr((((ord(letter) - 65) + x) % 26) + 65))
  print str(x) + ": " + ''.join(plaintext)
  return plaintext
