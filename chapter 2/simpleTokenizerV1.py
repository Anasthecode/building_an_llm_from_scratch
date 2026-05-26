import re

class SimpleTokenizerV1:
    def __init__(self, vocab):
        """Encoding and decoding are just using a map/dictionary
           Really speaking, their algorithm is nothing complex or hard"""
        self.strToInt = vocab
        self.intToStr = {i:s for s, i in vocab.items()}

    def encode(self, text):
      preprocessed = re.split(r'([,.:;?_!"()\']|--|\s)', text)
      preprocessed = [
      item.strip() for item in preprocessed if item.strip()
      ]
      ids = [self.strToInt[s] for s in preprocessed]
      return ids
    
    def decode(self, ids):
      text = " ".join([self.intToStr[i] for i in ids])
      text = re.sub(r'\s+([,.:;?!"()\'])', r'\1', text)
      return text