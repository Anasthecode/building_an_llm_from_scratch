from importlib.metadata import version
import os
import requests
import re

class HelperMethods:
  @staticmethod
  def readFile(cleanFile, url):
    if not os.path.exists(cleanFile):
      # Download and process the file
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
        print(f"Text saved to {cleanFile}")
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

    return novelText
  
  @staticmethod
  def makePreprocessed(novelText):
    preprocessed = re.split(r'([,.:;?_!"()\']|--|\s)', novelText) 
    preprocessed = [item.strip() for item in preprocessed if item.strip()]
    preprocessedSize = len(preprocessed)

    return preprocessed, preprocessedSize
  
  @staticmethod
  def makeVocabV1(preprocessed):
    allWords = sorted(set(preprocessed))
    vocabSize = len(allWords)

    vocab = {token: integer for integer, token in enumerate(allWords)}

    return vocab, vocabSize
  
  @staticmethod
  def makeVocabV2(preprocessed):
    allWords = sorted(set(preprocessed))
    allWords.extend(["<|endoftext|>", "<|unk|>"])
    vocabSize = len(allWords)

    vocab = {token: integer for integer, token in enumerate(allWords)}

    return vocab, vocabSize