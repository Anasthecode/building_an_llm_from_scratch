from importlib.metadata import version
import os
import requests
import re

print("torch version:", version("torch"))
print("tiktoken version:", version("tiktoken"))


print("Tokenization: Chapter 2.2")

cleanFile = "frankenstein_clean.txt"

if not os.path.exists(cleanFile):
    # Download and process the file
    url = "https://www.gutenberg.org/files/84/84-0.txt"
    print(f"Downloading from {url}...")
    response = requests.get(url)
    response.raise_for_status()
    rawText = response.text

    # Cleanup
    startMarker = "\n\nLetter 1\n"
    endMarker = "*** END OF THE PROJECT GUTENBERG EBOOK 84 ***"

    if startMarker in rawText and endMarker in rawText:
        novelText = rawText.split(startMarker)[1].split(endMarker)[0]
        novelText = novelText.strip()

        # Clean formatting BEFORE saving
        novelText = novelText.replace('_', '') # Getting rid of italics
        novelText = re.sub(r'\n\s*\n', '\n\n', novelText) # gettind rid of white space
        # no need to git rid of bold fonts (*) as the end/start markers involve that already

        with open(cleanFile, "w", encoding="utf-8") as f:
            f.write(novelText)
        print("Text saved to 'frankenstein_clean.txt'")
        print(f"Total characters: {len(novelText)}")
    else:
        print("Could not find the start/end markers in the download file")
        exit(1)
else:
    # File already exists scenario
    print(f"Loading existing {cleanFile}...")
    with open(cleanFile, "r", encoding="utf-8") as f:
        novelText = f.read()
    print(f"Loaded {len(novelText)} characters")

# I ended up using the same one as the book had, though it is slightly irrelevant as I did get rid of spaces in mine
preprocessed = re.split(r'([,.:;?_!"()\']|--|\s)', novelText) 
preprocessed = [item.strip() for item in preprocessed if item.strip()]
print(preprocessed[:50])
print(len(preprocessed))

# text = input("Try whatever, could use the example from the book: ")

# result = re.split(r'([,.:;?_!"()\']|--|\s)', text)
# result = [item.strip() for item in result if item.strip()]
# print(result)

print("Token to token IDs: Chapter 2.3")
allWords = sorted(set(preprocessed))
vocabSize = len(allWords)
#print(allWords)
print(vocabSize)

vocab = {token: integer for integer, token in enumerate(allWords)}
# for i, item in enumerate(vocab.items()):
#     print(item)
#     if i >= 50:
#         break

class SimpleTokenizerV1:
    def __init__(self, vocab):
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
    
tokenizer = SimpleTokenizerV1(vocab)

text = """But I have one want which I have never yet been able to satisfy, and the
absence of the object of which I now feel as a most severe evil, I have no
friend, Margaret: when I am glowing with the enthusiasm of success, there
will be none to participate my joy;"""

ids = tokenizer.encode(text)
print(ids)
print(tokenizer.decode(ids))
