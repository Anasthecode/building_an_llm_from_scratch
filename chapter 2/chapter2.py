from importlib.metadata import version

# My own files/classes
from helperMethods import HelperMethods
from simpleTokenizerV1 import SimpleTokenizerV1
from simpleTokenizerV2 import SimpleTokenizerV2

print("torch version:", version("torch"))
print("tiktoken version:", version("tiktoken"))

# I picked frankenstein for this, book was the cadaver, any piece of text works
print("Tokenization: Chapter 2.2")
cleanFile = "frankenstein_clean.txt"
url = "https://www.gutenberg.org/files/84/84-0.txt"

novelText = HelperMethods.readFile(cleanFile, url)

# I ended up using the same one as the book had, though it is slightly irrelevant as I did get rid of spaces in mine
preprocessed, preprocessedSize = HelperMethods.makePreprocessed(novelText)
print("Preprocessed words: ", preprocessed[:50])
print("Preprocessed words size: ", preprocessedSize)

# text = input("Try whatever, could use the example from the book: ")
# test = HelperMethods.makePreprocessed(text)
# print(test)

print("Token to token IDs: Chapter 2.3")
allWords = sorted(set(preprocessed))
"""The lines below are a new addition.
   Their purpose is to provide a failsafe
   incase the input is not in the vocabulary
   Design principle: do more for fails than just rejection"""
allWords.extend(["<|endoftext|>", "<|unk|>"])
vocabSize = len(allWords)
#print(allWords)
print("Size of the vocabulary: ", vocabSize)
print("Change between vocabulary size and the preprocessed: ", preprocessedSize - vocabSize)

vocab = {token: integer for integer, token in enumerate(allWords)}
# print(vocab)

# for i, item in enumerate(vocab.items()):
#     print(item)
#     if i >= 50:
#         break
    
tokenizer = SimpleTokenizerV1(vocab)

text = """But I have one want which I have never yet been able to satisfy, and the
absence of the object of which I now feel as a most severe evil, I have no
friend, Margaret: when I am glowing with the enthusiasm of success, there
will be none to participate my joy;"""

ids = tokenizer.encode(text)
print(ids)
print(tokenizer.decode(ids))

text1 = "Hello, do you like tea?"
text2 = "In the sunlit terraces of the palace."
text = " <|endoftext|> ".join((text1, text2))
print("Practice text: ", text)

tokenizer = SimpleTokenizerV2(vocab)
print("Encoding: ", tokenizer.encode(text))
print("Decoding: ", tokenizer.decode(tokenizer.encode(text)))
