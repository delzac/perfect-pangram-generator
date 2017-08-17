# Perfect Pangram Generator

Generates perfect pangrams (sentences where every letter of the alphabet is represented exactly once).

Improvements:

1) The heuristic could be developed further. In particular, I think vowel density could help out.

2) You could implement some memoization of word combination, or figure out another way to filter duplicate permutations of words.

3) THe dictionary could be preprocessed such that it automatically filters all words with duplicate letters, and other optimizations.