from importlib.metadata import version
import tiktoken

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
vocabV1, vocabSizeV1 = HelperMethods.makeVocabV1(preprocessed)
print("Size of vocabulary V1: ", vocabSizeV1)
print("Change between vocabulary size and the preprocessed: ", preprocessedSize - vocabSizeV1)

# for i, item in enumerate(vocab.items()):
#     print(item)
#     if i >= 50:
#         break
    
tokenizer = SimpleTokenizerV1(vocabV1)

text = """But I have one want which I have never yet been able to satisfy, and the
absence of the object of which I now feel as a most severe evil, I have no
friend, Margaret: when I am glowing with the enthusiasm of success, there
will be none to participate my joy;"""

ids = tokenizer.encode(text)
print("IDs of version 1: ", ids)
print("Decoding of version 1: ", tokenizer.decode(ids))

vocabV2, vocabSizeV2 = HelperMethods.makeVocabV2(preprocessed)
print("Size of vocabulary V2: ", vocabSizeV2)
print("Change between vocabulary size and the preprocessed: ", preprocessedSize - vocabSizeV2)

text1 = "Hello, do you like tea?"
text2 = "In the sunlit terraces of the palace."
text = " <|endoftext|> ".join((text1, text2))
print("Practice text for version 2: ", text)

tokenizer = SimpleTokenizerV2(vocabV2)
print("Encoding: ", tokenizer.encode(text))
print("Decoding: ", tokenizer.decode(tokenizer.encode(text)))



tokenizer = tiktoken.get_encoding("gpt2")
# text = ( # This is from the book, not mine
#  "Hello, do you like tea? <|endoftext|> In the sunlit terraces"
#  "of someunknownPlace."
# )
# integers = tokenizer.encode(text, allowed_special={"<|endoftext|>"})
# print(integers)
# integers = tokenizer.encode("Akwirw ier")
# print(integers)

encText = tokenizer.encode(novelText)
print(len(encText))

