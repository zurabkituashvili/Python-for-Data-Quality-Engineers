import re

# 1) Copy the text into a variable
text = """
  tHis iz your homeWork, copy these Text to variable.
  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.
  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.
  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.

"""

# replace only the whole word "iz", not parts of other words
fixed_text = re.sub(r"\biz\b", "is", text, flags=re.IGNORECASE)

# Split text into sentences while keeping punctuation
parts = re.split(r"([.!?])", fixed_text)

sentences = []
for i in range(0, len(parts) - 1, 2):
    sentence = parts[i].strip()
    punctuation = parts[i + 1]

    if sentence:
        sentence = sentence.lower()
        sentence = sentence[0].upper() + sentence[1:]
        sentences.append(sentence + punctuation)

# Create one more sentence from the last word of each existing sentence
last_words = []
for sentence in sentences:
    words = re.findall(r"[A-Za-z0-9]+", sentence)
    if words:
        last_words.append(words[-1])

new_sentence = " ".join(last_words).capitalize() + "."

# Add the new sentence to the end of the paragraph
final_text = " ".join(sentences) + " " + new_sentence

# Count all whitespace characters in the original text
whitespace_count = sum(1 for ch in text if ch.isspace())

# Output
print("Normalized text:")
print(final_text)
print()
print("Whitespace characters:", whitespace_count)
