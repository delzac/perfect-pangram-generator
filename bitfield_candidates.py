import re
import sys
from bitfield_dp import bitfields_dynamic_programming
from bitfield_powerset import find_subsets_backtracking

is_lowercase_letters = re.compile('^[a-z_\-]+$')

LETTER_FREQUENCIES = {
  "e": 25,
  "t": 24,
  "a": 23,
  "o": 22,
  "i": 21,
  "n": 20,
  "s": 19,
  "h": 18,
  "r": 17,
  "d": 16,
  "l": 15,
  "c": 14,
  "u": 13,
  "m": 12,
  "w": 11,
  "f": 10,
  "g": 9,
  "y": 8,
  "p": 7,
  "b": 6,
  "v": 5,
  "k": 4,
  "j": 3,
  "x": 2,
  "q": 1,
  "z": 0
}

def word_to_bitfield(word):
  word = word.lower()
  if not is_lowercase_letters.match(word):
    return False
  bitfield = 0
  for character in word:
    index = LETTER_FREQUENCIES[character]
    shifted = (1 << index)
    if bitfield & shifted:
      return False
    bitfield = bitfield | shifted
  return bitfield

# assuming a word-per-line dictionary with no dupes
def read_dictionary_file(filename):
  bitfield_dictionary = {}
  with open(filename) as f:
    for word in f:
      word = word.strip()
      bitfield = word_to_bitfield(word)
      if bitfield != False:
        if bitfield_dictionary.get(bitfield) == None:
          bitfield_dictionary[bitfield] = []
        bitfield_dictionary[bitfield].append(word)
  return bitfield_dictionary

def find_first_letter(bitfield):
  first_letter = 0
  while bitfield & 1 == 0:
    first_letter += 1
    bitfield = bitfield >> 1
  
  return first_letter

def find_first_letter_needed(bitfield):
  first_letter = 0
  while bitfield & 1 == 1:
    first_letter += 1
    bitfield = bitfield >> 1
  
  return first_letter

def pangrams_from_radix(radixes, objective, accumulated=0, words=[]):
  if accumulated == objective:
    print words
    return

  first_letter_needed = find_first_letter_needed(accumulated)
  bitfields_with_letter = radixes[first_letter_needed]

  for bitfield in bitfields_with_letter:
    if accumulated & bitfield == 0:
      pangrams_from_radix(radixes, objective, accumulated | bitfield, words + [bitfield])

def generate_pangrams(bitfield_dictionary):
  # find all combinations of keys that mask to 26 'one' bits
  bitfield_keys = bitfield_dictionary.keys()

  radixes = []
  for i in range(26):
    radixes.append([])

  for bitfield in bitfield_keys:
    first_letter = find_first_letter(bitfield)
    radixes[first_letter].append(bitfield)

  saturated_bitmask = (1 << 26) - 1
  
  pangrams_from_radix(radixes, saturated_bitmask)

if __name__ == "__main__":
  filename = "tests/scrabble-dictionary.txt"
  if len(sys.argv) > 1:
    filename = sys.argv[1]
  bitfield_dictionary = read_dictionary_file(filename)
  generate_pangrams(bitfield_dictionary)
