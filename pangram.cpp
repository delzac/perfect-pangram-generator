#include <queue>
#include <vector>
#include <iostream>
#include <string>
#include <fstream>
#include <unordered_map>
#include <set>
 
template<typename T> void print_queue(T& q) {
    while(!q.empty()) {
        std::cout << q.top() << " ";
        q.pop();
    }
    std::cout << '\n';
}

std::vector<std::string> readFileToVector(const std::string& filename)
{
    std::ifstream source;
    source.open(filename);
    std::vector<std::string> lines;
    std::string line;
    while (std::getline(source, line))
    {
        lines.push_back(line);
    }
    return lines;
}

int points(std::string& sentence) {
  return sentence.size();
}

class Heuristic {
public:
    bool operator()(std::string& a, std::string& b)
    {
       return (points(a) < points(b));
    }
};

bool hasDuplicates(std::string& sentence) {
  std::set<char> letters = {};
  for(char& c : sentence) {
    auto contains = letters.find(c) != letters.end();
    if (!contains) {
      letters.insert(c);
    } else {
      return true;
    }
  }

  return false;
}

bool isPangram(std::string& sentence) {
  std::set<char> alphabet = {
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y', 'z'
  };

  std::set<char> letters;
  for(char& c : sentence) {
    letters.insert(c);
  }

  return letters == alphabet;
}

void conditionallyInsert(std::string& sentence, std::priority_queue<std::string, std::vector<std::string>, Heuristic>& q) {
  if (!hasDuplicates(sentence)) {
    q.push(sentence);
  }
}

std::vector<std::string> getCandidates(std::string& sentence, std::vector<std::string>& words) {
  std::vector<std::string> newCandidates = {};
  for(std::string s : words)
    newCandidates.push_back(sentence + s);

  return newCandidates;
}

int main(int argc, char **argv) {
    std::priority_queue<std::string, std::vector<std::string>, Heuristic> q;
    std::vector<std::string> words = readFileToVector(argv[1]);
 
    for(std::string s : words)
        conditionallyInsert(s, q);

    while (!q.empty()) {
      std::string candidate = q.top();
      if (isPangram(candidate)) {
        std::cout << "candidate found!" << '\n';
        std::cout << candidate << '\n';
        return 0;
      }
      std::vector<std::string> newCandidates = getCandidates(candidate, words);
      q.pop();
      for(std::string s : newCandidates)
        conditionallyInsert(s, q);
    }

    std::cout << "no candidates found!" << '\n';
    return 0;
}