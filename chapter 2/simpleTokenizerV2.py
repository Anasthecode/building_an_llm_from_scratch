import re

class SimpleTokenizerV2:
    """"Only upgrade is that we now account for non-vocab words"""
    def __init__(self, vocab):
        self.strToInt = vocab
        self.intToStr = {i:s for s,i in vocab.items()}
    
    def encode(self, text):
        preprocessed = re.split(r'([,.:;?_!"()\']|--|\s)', text)
        preprocessed = [
        item.strip() for item in preprocessed if item.strip()
        ]
        preprocessed = [item if item in self.strToInt
        else "<|unk|>" for item in preprocessed]
        ids = [self.strToInt[s] for s in preprocessed]
        return ids
    
    def decode(self, ids):
        text = " ".join([self.intToStr[i] for i in ids])
        text = re.sub(r'\s+([,.:;?!"()\'])', r'\1', text)
        return text