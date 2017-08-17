#!/usr/bin/env bash
# usage: test.sh {TEST DICTIONARY}

echo TESTING $1
g++ -std=c++11 pangram.cpp -o pangram && ./pangram $1
