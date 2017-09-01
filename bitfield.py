import re
import sys

is_lowercase_letters = re.compile('^[a-z_\-]+$')
ALPHABET_LENGTH = 26

LETTER_FREQUENCIES = {
  "e": 0,
  "t": 1,
  "a": 2,
  "o": 3,
  "i": 4,
  "n": 5,
  "s": 6,
  "h": 7,
  "r": 8,
  "d": 9,
  "l": 10,
  "c": 11,
  "u": 12,
  "m": 13,
  "w": 14,
  "f": 15,
  "g": 16,
  "y": 17,
  "p": 18,
  "b": 19,
  "v": 20,
  "k": 21,
  "j": 22,
  "x": 23,
  "q": 24,
  "z": 25
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

def find_subsets_backtracking(bitfields, objective):
    stack = [(bitfields, 0, [])]

    while stack:
      array, accumulated, subset = stack.pop()

      if accumulated > objective:
          continue
      if accumulated == objective:
        yield subset
        continue

      if len(array) == 0:
          continue

      if accumulated & array[0] == 0:
        included = accumulated | array[0]
        stack.append((array[1:], included, subset + [array[0]]))

      enough_bits_left = accumulated
      for number in array:
        enough_bits_left = enough_bits_left | number
        if enough_bits_left >= objective:
          stack.append((array[1:], accumulated, subset))
          break

def generate_pangrams(bitfield_dictionary, alphabet_length = ALPHABET_LENGTH):
  # find all combinations of keys that mask to 26 'one' bits
  bitfield_keys = bitfield_dictionary.keys()
  bitfield_keys.sort(reverse=True)
  saturated_mask = (1 << alphabet_length) - 1

  for solution in find_subsets_backtracking(bitfield_keys, saturated_mask):
    yield solution

if __name__ == "__main__":
  filename = "tests/scrabble-dictionary.txt"
  bitfield_dictionary = read_dictionary_file(filename)
  for pangram in generate_pangrams(bitfield_dictionary):
    print pangram
