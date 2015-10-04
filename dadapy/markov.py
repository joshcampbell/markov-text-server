import json
import random
import string
import sys

from Queue import Queue

from dadapy.cleaner import clean

class nGramBuffer:
    """ Mutable n-gram class for use in markov dictionaries.
        the idea is that it's filled one word at a time as
        we iterate across the source text.
    """

    def __init__(self, n):
        self.n = n
        self.words = []

    def is_full(self):
        return len(self.words) == self.n

    def cycle(self, word):
        if self.is_full():
            self.words.remove(self.words[0])
        self.words.append(word)

    def as_key(self):
        return string.join(self.words)

    def as_pair(self):
        return (self.words[0:-1], self.words[-1])

    def as_key(self):
        pair = self.as_pair()
        return string.join(pair[0])

    def as_list(self):
        return self.words

    def last_word(self):
        return self.words[-1]

class MarkovDictionary:
    """ Manages a nested dict of word occurance probabilities """
    def __init__(self, source_text=None, depth=2):
      # there must be at least depth + 1 words in the source text
      # depth cannot be less than 2
      self.depth = depth
      self.key_length = self.depth - 1
      self.ngrams = {}
      if source_text != None:
        self.engorge(source_text)

    def engorge(self, source_text):
      words = clean(source_text).split()
      window = nGramBuffer(self.depth)
      for word in words:
          window.cycle(word) 
          if window.is_full():
              self.__upsert_buffer(window)
      # handle special case - first word should follow last key
      window.cycle(words[0])
      self.__upsert_buffer(window)
      # handle another special case (one window should straddle text boundry)
      window.cycle(words[1])
      self.__upsert_buffer(window)

    def __upsert_buffer(self, ngram_buffer):
      key = ngram_buffer.as_key()
      val = ngram_buffer.last_word()
      if self.ngrams.get(key, None) == None:
          self.ngrams[key] = {}
      if self.ngrams[key].get(val, None) == None:
          self.ngrams[key][val] = 0
      self.ngrams[key][val] += 1

    def get_lexicon(self):
      words = []
      for word_dict in self.ngrams.values():
        words += word_dict.keys()
      return words

    def __last_ngram_index(self):
      return -1 * (self.key_length)

    def __last_ngram(self, word_list):
      last_ngram_index = self.__last_ngram_index()
      return word_list[last_ngram_index:]

    def disgorge(self, length=600):
      # TODO: special case handling for length < depth
      word_list = random.choice(self.ngrams.keys()).split()
      for i in range(0, length - self.key_length): 
        if(len(word_list) == self.key_length):
            key = string.join(word_list)
        else:
            key = string.join(self.__last_ngram(word_list))
        followers = self.ngrams[key]
        word_list.append(random.choice(followers.keys()))
      return string.join(word_list)
