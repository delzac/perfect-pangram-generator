import re
import sys
from bitfield_dp import bitfields_dynamic_programming
from bitfield_powerset import find_subsets_backtracking

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


class Bitfield_Trie:
  class bitfield_node():
    def __init__(self):
      self.value = None
      self.left = None
      self.right = None

  def __init__(self):
    self.root = bitfield_node()

  def insert_bitfield(self, bitfield):
    curr_node = self.root
    while bitfield > 0:
      if bitfield & 1:
        if curr_node.right is not None:
          curr_node = curr_node.right
        else:
          new_node = bitfield_node()
          curr_node.right = new_node
          curr_node = new_node
      else:
        if curr_node.left is not None:
          curr_node = curr_node.left
        else:
          new_node = bitfield_node()
          curr_node.left = new_node
          curr_node = new_node
      bitfield = bitfield >> 1
  
  def get_bitfield(self, bitfield):
    curr_node = self.root
    while bitfield > 0:
      if bitfield & 1:
        if curr_node.right is not None:
          curr_node = curr_node.right
        else:
          return None
      else:
        if curr_node.left is not None:
          curr_node = curr_node.left
        else:
          return None
      bitfield = bitfield >> 1
    return curr_node

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
  bitfield_trie = Bitfield_Trie()
  with open(filename) as f:
    for word in f:
      word = word.strip()
      bitfield = word_to_bitfield(word)
      if bitfield != False:
        bitfield_trie.insert_bitfield(bitfield)
  return bitfield_trie

if __name__ == "__main__":
  filename = "tests/scrabble-dictionary.txt"
  if len(sys.argv > 1):
    filename = sys.argv[1]
  bitfield_trie = read_dictionary_file(filename)
