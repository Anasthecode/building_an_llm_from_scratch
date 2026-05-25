from importlib.metadata import version
import os
import requests

print("torch version:", version("torch"))
print("tiktoken version:", version("tiktoken"))

url = "https://www.gutenberg.org/files/84/84-0.txt"
print(f"Downloading from {url}...")
response = requests.get(url)
response.raise_for_status()
rawText = response.text

# cleanup, making sure it is only learning off of Frankenstein
startMarker = "*** START OF THE PROJECT GUTENBERG EBOOK 84 ***"
endMarker = "*** END OF THE PROJECT GUTENBERG EBOOK 84 ***"

if startMarker in rawText and endMarker in rawText:
  novelText = rawText.split(startMarker)[1].split(endMarker)[0]
  novelText = novelText.strip()

  with open("frankenstrein_clean.txt", "w", encoding="utf-8") as f:
    f.write(novelText)
  print("Text saved to 'frankenstein_clean.txt'")
  print(f"Total characters: {len(novelText)}")
else:
  print("Could not find the start/end markers in the download file")

