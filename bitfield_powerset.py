def find_last_one_bit(number):
  last_one_bit_index = 0      
  while number > 0:
    number = number >> 1
    last_one_bit_index += 1
  return last_one_bit_index

def find_last_zero_bit(number):
  last_zero_bit_index = 0
  current_bit_index = 0
  while number > 0:
    if number & 1 == 0:
      last_zero_bit_index = current_bit_index
    number = number >> 1
    current_bit_index += 1
  return last_zero_bit_index

calls = 0

# assumes a reverse ordered bitfield array
# TODO: reduce array copies
def find_subsets_backtracking(bitfields, objective):
  global calls
  stack = [(bitfields, 0, [])]

  while stack:
    calls += 1
    array, accumulated, subset = stack.pop()

    if accumulated > objective:
        continue
    if accumulated == objective:
      yield subset
      continue

    array_length = len(array)
    if array_length == 0:
        continue


    # only include a subset that doesn't include the current bitfield
    # if we're sure that there'll be enough bits in the ensuing subset
    # to or to a saturated bitmask
    if array_length > 1:
      last_zero_in_accumulated_index = find_last_zero_bit(accumulated)
      has_enough_bits = array[1]
      has_enough_bits_index = find_last_one_bit(has_enough_bits)
      if has_enough_bits_index >= last_zero_in_accumulated_index:
        stack.append((array[1:], accumulated, subset))
    
    included = accumulated | array[0]
    filtered = []
    for bitfield in array[1:]:
      # only include this one in the subset if it wouldn't collide with a used letter
      if bitfield & included == 0:
        filtered.append(bitfield)
    stack.append((filtered, included, subset + [array[0]]))

if __name__ == "__main__":
  def binary_format(num):
    return format(num, '026b')

  def test(objective, bitmasks):
    global calls
    calls = 0
    print "testing: %s" % binary_format(objective)
    for pangram in find_subsets_backtracking(bitmasks, objective):
      print map(binary_format, pangram)
    print "calls: %s" % calls

  saturated_bitmask = (1 << 26) - 1
  alphabet = []
  for i in range(26):
    alphabet.append(1 << i)
  alphabet.reverse()
  test(saturated_bitmask, alphabet)