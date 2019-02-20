# re is a Python module for parsing a Regex (Character filter)
import re

"""
Reads a file and counts the occurrences of each character, A-Z
while ignoring letter case and non-alphabetical characters

Prints a frequency analysis for each letter
as well as the Index of Coincidence
"""
def analyzeFile(file):
  # Reads the contents of the file as a string
  contents = open(file, 'r').read()
  # Makes 'contents' all uppercase
  contents = contents.upper()
  # Removes any non-A-Z character (regex of ^[A-Z])
  contents = re.sub(r'(^[A-Z])', '', contents)
  # Saves the length of the contents for when we calculate the IoC
  length = len(contents)

  # This creates a list of letters in the alphabet
  # paired with a counter initially set to '0'
  alphabet = [list(pair) for pair in zip(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"), 26*[0])]

  # Below is a nested loop that counts the letter frequencies
  # For each letter in the contents of the file
  for letter in contents:
    # For each index of each letter in the alphabet (0-25)
    for index in range(26):
      # If the letter matches the current character index of the alphabet
      if alphabet[index][0] == letter:
        # Add one to the matched letter frequency counter
        alphabet[index][1] += 1

  # Index of Coincidence, sum of (freq * (freq - 1)) / (length * (length - 1))
  ioc = 0.0
  # For each letter and counter pair of the alphabet
  for pair in alphabet:
    # Add our calculated individual letter frequency to the IoC
    ioc += (pair[1] * (pair[1] - 1.)) / (length * (length - 1.))
    # Print the letter and its frequency
    print pair[0] + ": %d" % pair[1]
  # Prints the calculated IoC to 4 places
  print "IoC: %.4f\n" % ioc
