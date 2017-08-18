# Perfect Pangram Generator

Generates perfect pangrams (sentences where every letter of the alphabet is represented exactly once).

Improvements:

1) The heuristic could be developed further. In particular, I think vowel density could help out.

2) You could implement some memoization of word combination, or figure out another way to filter duplicate permutations of words.

3) The dictionary could be preprocessed such that it automatically filters all words with duplicate letters, and other optimizations.

4) Dictionary could be preprocessed such that all words are sorted by rarity of letter. Words containing the rarest letter are put in the priority queue first, and then when popped off, matched with all words that contain the next rarest letter that the word doesn't have.