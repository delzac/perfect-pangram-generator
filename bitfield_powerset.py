# assumes a reverse ordered bitfield array
def find_subsets_backtracking(bitfields, objective):
  stack = [(bitfields, 0, [])]

  while stack:
    array, accumulated, subset = stack.pop()

    if accumulated > objective:
        continue
    if accumulated == objective:
      yield subset
      continue

    array_length = len(array)
    if array_length == 0:
        continue

    if accumulated & array[0] == 0:
      included = accumulated | array[0]
      stack.append((array[1:], included, subset + [array[0]]))

    # only keep trying subsets that have enough bits to saturate the objective
    # this only works because we assume a reverse ordered bitfield array
    if array_length > 1 and array[1] >= (objective >> 1):
      stack.append((array[1:], accumulated, subset))
      break

if __name__ == "__main__":
  saturated_bitmask = (1 << 26) - 1
  alphabet = []
  for i in range(26):
    alphabet.append(1 << i)
  alphabet.reverse()
  for pangram in find_subsets_backtracking(alphabet, saturated_bitmask):
    print pangram