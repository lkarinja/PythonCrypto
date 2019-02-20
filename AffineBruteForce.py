def affine(ciphertext):
  # Affine Ciphers can have a 'b' between 0 and 25 inclusively
  for b in range(0,26):
    # Affine Ciphers can have an 'a' that is relatively prime with 26
    for a in [1,3,5,7,9,11,15,17,19,21,23,25]:
      # This is where we store our decrypted plaintext
      plaintext=list()
      # For each letter in the ciphertext
      for letter in ciphertext:
        # Our next plaintext character is calculated by 'plaintext = (ciphertext - b) * a MOD 26
        # We need to subtract and add 65 as this is the diff between A~B being 0~25 and ASCII
        plaintext.append(chr(((((ord(letter) - 65) + b) * a) % 26) + 65))
      # This makes the plaintext a string instead of a list of letters
      plaintext = ''.join(plaintext)
      # We can narrow down the results by searching for keywords
      # such as 'THE', 'BE', 'TO', 'OF', or 'AND'
      if any(word in plaintext for word in ['THE', 'BE', 'TO', 'OF', 'AND']):
        # Print the 'a' and 'b' value that gives the plaintext
        print "a:" + str(a) + "b" + str(b) + ": " + plaintext
