from typing import Iterator, Tuple

def isEmptyOrWhitespaces(self: str) -> bool:
  return (len(self) == 0 or len(self.strip()) == 0)  

def find_all(self: str, pattern: str) -> Iterator[Tuple[int, str]]:
  '''Yields all the positions of the pattern in string.'''
  # base case: the first search, if pattern is not found, while loop will be skipped and the iterator will be empty
  i = self.find(pattern)

  # loop: continue the search and return more matches
  while i != -1:
    yield i
    i = self.find(pattern, i + 1)