# Copyright 2019, Leejae Karinja, All rights reserved.

# re is used for parsing a Regex (Character filter)
# copy is used to copy lists to prevent referenced object changes
# math is used for rounding up/down
import re, copy, math

"""
Reads a file and counts the occurrences of each character, A-Z
while ignoring letter case and non-alphabetical characters

Prints a frequency analysis and occurrences for each letter
as well as the Index of Coincidence, then tries to estimate a key
and use it to decrypt the provided text

Returns the estimated plaintext
"""
def analyzeFile(file):
  # Print the name of the file we will analyze
  print ("#" * (len(file) + 12) + "\n#ANALYZING %s#\n" + "#" * (len(file) + 12)) % file

  # Reads the contents of the file as a string
  contents = open(file, 'r').read()
  # Makes 'contents' all uppercase
  contents = contents.upper()
  # Removes any non-A-Z character (regex of (?![A-Z]).)
  contents = re.sub('(?![A-Z]).', '', contents)
  # Saves the length of the contents for when we calculate the IoC
  length = len(contents)

  # Count the occurrences of each letter in the given text
  counted = countLetters(contents);
  # Calculates letter frequency given letter occurrences and total length
  freq = calcFreq(counted, length)

  # Stores the Index of Coincidence
  ioc = 0.0

  # For each letter of the alphabet
  for letter in range(26):
    # Add our calculated individual letter frequency to the IoC
    ioc += (counted[letter][1] * (counted[letter][1] - 1.)) / (length * (length - 1.))
    # Print the letter with its frequency (to 4 places) and occurrences
    print freq[letter][0] + ": Frequency(%.4f) Occurrences(%d)" % (freq[letter][1], counted[letter][1])

  # Prints the calculated IoC to 4 places
  print "\nIoC: %.4f" % ioc

  # Calculates an estimate for the length of the key
  key_length = calcKeyLength(contents, length, ioc)

  # Prints the estimated key length
  print "\nEstimated Key Length: %d" % key_length

  # Stores the shifts (letters) that are most likely in the original key
  shifts = list()

  # For each possible shift (letter) in the key
  for shift in range(key_length):
    # Get a count of letter occurrences in a subset of ever 'shift'th letter
    subset_count = countLetters(contents[shift::key_length])
    # Calculate the dot product of letter frequency of the given subset and English
    subset_freq = dotFrequency(calcFreq(subset_count, len(subset_count)))
    # Save the estimated shift (letter) that was used in the original key
    shifts.append(subset_freq)

  # Save the estimated key as a string
  key = ''.join([chr(char + 65) for char in shifts])
  # Calculate and save the estimated plaintext, decrypted with the given key
  plaintext = decrypt(contents, key)

  # Prints the estimated key
  print "\nThe estimated key is: %s" % key
  # Prints the estimated plaintext
  print "\nThe plaintext could be:\n%s" % plaintext

  # Print that we have finished analyzing the file
  print ("#" * (len(file) + 21) + "\n#FINISHED ANALYZING %s#\n" + "#" * (len(file) + 21) + "\n") % file

  # Return the estimated plaintext
  return plaintext

"""
Counts the occurrences of each letter of the alphabet in the supplied text
and then returns a list of the letters and their occurrences
"""
def countLetters(contents):
  # Stores a list of letters along with a running counter of their occurrences
  alphabet = [list(pair) for pair in zip(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"), 26*[0])]

  # For each letter in the contents of the file
  for letter in contents:
    # For each index of each letter in the alphabet (0-25)
    for index in range(26):
      # If the letter matches the current character index of the alphabet
      if alphabet[index][0] == letter:
        # Add one to the matched letter frequency counter
        alphabet[index][1] += 1

  # Returns the calculated letter frequencies
  return alphabet

"""
Calculates letter frequency given a list of occurrences
for each letter in the alphabet as well as the total number
of letters that occurred, then returns a list of the frequencies
"""
def calcFreq(counted, length):
  # Makes a copy of the counted alphabetic list to prevent reference changes
  freq = copy.deepcopy(counted)

  # For each letter and its number of occurrences
  for pair in freq:
    # Calculate the frequency of the letter across the entire text
    pair[1] /= float(length)

  # Return the list of calculated letter frequencies
  return freq

"""
Calculates an estimate for the key length for the given ciphertext
and returns the estimated length

This method will replace the Friedman Test, which is the following
((0.0265 * length) / ((0.065 - ioc) + (ioc - 0.0385) * length))
and is used as a shot in the dark key length
"""
def calcKeyLength(ciphertext, length, ioc):
  # Calculate a base approximation of the key length using the Friedman Test
  friedman = ((0.0265 * length) / ((0.065 - ioc) + (ioc - 0.0385) * length))
  # Print our initial approximate key length
  print "\nFriedman Test Key Length Approximation: %.4f" % friedman

  # If the Friedman Test results in a key that is at or less than 1
  if friedman <= 1.0:
    # They key is most likely a single character (or a Caesar Cipher)
    return 1

  # Stores average IoCs given estimated key lengths, higher is better
  average_iocs = list()

  # For possible key lengths between 1 and our Friedman approximation
  for possible_length in range(1, int(math.ceil(friedman)) + 1):
    # Stores the IoCs of given key length segments
    iocs = list()

    # For each group of every 'possible_length'th letter
    for starting_shift in range(possible_length):
      # Get every 'possible_length'th letter
      subset = ciphertext[starting_shift::possible_length]
      # Get a count of letter occurrences
      count = countLetters(subset)
      # Gets the total number of letters in each iterated group
      length = reduce((lambda a, b: a + b), [pair[1] for pair in count])

      # Stores the calculated IoC
      ioc = 0.0

      # For each letter in the alphabet
      for letter in range(26):
        # Update our calculation for the IoC
        ioc += (count[letter][1] * (count[letter][1] - 1.)) / (length * (length - 1.))
      # Add this IoC to the other IoCs of the same keyword length with different groupings
      iocs.append(ioc)
    # Average the IoCs of a given key length
    average_iocs.append((reduce((lambda a, b: a + b), iocs) / possible_length))

  # Return the estimated key length
  return average_iocs.index(max(average_iocs)) + 1

"""
Calculates the dot product of a given letter frequency list
and the Scrawl of English to attempt to find the correct
shift of letters, then returns the approximated shift
"""
def dotFrequency(freq):
  # Scrawl of English as a list
  scrawl = [list(pair) for pair in zip(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"), [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150, 0.01974, 0.00074])]
  # Stores the dot product of each shift of the alphabet
  dots = 26*[0]

  # For each possible shift of the alphabet
  for shift in range(26):
    # Stores the running total for the dot product
    dot = 0.0

    # For each letter in the alphabet
    for letter in range(26):
      # Add the product of the given letter frequency and the Scrawl of English to the dot
      dot += freq[letter][1] * scrawl[letter][1]

    # Store the dot product for the given shift
    dots[shift] = dot
    # Shifts the given letter frequency list over for the next dot product
    freq.append(freq.pop(0))

  # Return the shift with the max dot product, which is likely the correct shift
  return dots.index(max(dots))

"""
Decrypts ciphertext that was encrypted with a Vigenere Cipher
using the specified key and returns the plaintext
"""
def decrypt(ciphertext, key):
  # Stores the decrypted plaintext
  plaintext = list()

  # For each letter in the ciphertext
  for letter in range(len(ciphertext)):
    # Append the decrypted character to the plaintext
    plaintext.append(chr((((ord(ciphertext[letter]) - 65) - (ord(key[letter % len(key)]) - 65)) % 26) + 65))

  # Returns the decrypted text as a string
  return ''.join(plaintext)

# Analyze the provided files
analyzeFile('YOUR FILE HERE.txt')
