import re
import sys

is_lowercase_letters = re.compile('^[a-z_\-]+$')
ALPHABET_LENGTH = 26

def word_to_bitfield(word):
  word = word.lower()
  if not is_lowercase_letters.match(word):
    return False
  bitfield = 0
  for character in word:
    index = ord(character) - ord('a')
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

def generate_pangrams(bitfield_dictionary):
  # find all combinations of keys that mask to 26 'one' bits
  bitfield_keys = bitfield_dictionary.keys()
  saturated_mask = (1 << 26) -1

  def find_sums(objective, weights, memo={}):
    if objective <= 0:
      return []

    if not weights:
      return []

    memod = memo.get(objective)
    if memod is not None:
      return memod

    results = []
    for weight in weights:
      objective_difference = objective - weight
      without_weight = [x for x in weights if x != weight]
      sums = find_sums(objective_difference, without_weight, memo)
      for sum in sums:
        # sum is a list, python operators have confusing semantics
        results.append(sum + weight)
    
    memod[objective] = results
    return results

  return find_sums(saturated_mask, bitfield_keys)

if __name__ == "__main__":
  filename = sys.argv[1]
  bitfield_dictionary = read_dictionary_file(filename)
  for pangram in generate_pangrams(bitfield_dictionary):
    print pangram
