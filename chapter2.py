from importlib.metadata import version
import os
import requests
import re

print("torch version:", version("torch"))
print("tiktoken version:", version("tiktoken"))

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
