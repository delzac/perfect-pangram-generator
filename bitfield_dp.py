# assume: bitfields are reverse ordered
def bitfields_dynamic_programming(bitfields, objective, memo={}):
  memod = memo.get(objective)
  if memod is not None:
    return memod

  if objective <= 0:
    return []

  if not bitfields:
    return []
  
  # find every bitfield that ors to the complement
  results = []
  for bitfield in bitfields:
    # if the objective is the bitfield, add it
    if objective == bitfield:
      results.append([bitfield])
    # there are no duplicate letters
    elif objective & bitfield == bitfield:
      complement = objective ^ bitfield
      # impose an ordering to get unique subsets
      # we can do this because we've already found the greater complement
      if complement < bitfield:
        filtered_bitfield = [x for x in bitfields if x <= complement]
        complement_subsets = bitfields_dynamic_programming(filtered_bitfield, complement, memo)
        for subset in complement_subsets:
          results.append(subset + [bitfield])

  memo[objective] = results
  return results

if __name__ == "__main__":
  saturated_bitmask = (1 << 26) - 1
  alphabet = []
  for i in range(26):
    alphabet.append(1 << i)
  alphabet.reverse()
  test = bitfields_dynamic_programming(alphabet, saturated_bitmask)
  print format(saturated_bitmask, '026b'), ": ", test
