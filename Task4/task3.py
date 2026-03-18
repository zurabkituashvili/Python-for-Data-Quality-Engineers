import re
from typing import List


TEXT = """
  tHis iz your homeWork, copy these Text to variable.
  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.
  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.
  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.

"""


def fix_misspelling(text: str) -> str:
    # Replace only the standalone word 'iz' with 'is'.
    return re.sub(r"\biz\b", "is", text, flags=re.IGNORECASE)


def split_into_sentences(text: str) -> List[str]:
    # Split text into sentences while preserving punctuation.
    parts = re.split(r"([.!?])", text)
    sentences: List[str] = []

    for index in range(0, len(parts) - 1, 2):
        sentence_body = parts[index].strip()
        punctuation = parts[index + 1]

        if sentence_body:
            sentences.append(f"{sentence_body}{punctuation}")

    return sentences


def normalize_sentence_case(sentence: str) -> str:
    # Normalize sentence casing.
    normalized = sentence.lower()
    return normalized[0].upper() + normalized[1:] if normalized else normalized


def normalize_sentences(sentences: List[str]) -> List[str]:
    # Apply case normalization to all sentences.
    return [normalize_sentence_case(sentence) for sentence in sentences]


def extract_last_words(sentences: List[str]) -> List[str]:
    # Extract the last word from each sentence.
    last_words: List[str] = []

    for sentence in sentences:
        words = re.findall(r"[A-Za-z0-9]+", sentence)
        if words:
            last_words.append(words[-1])

    return last_words


def build_last_words_sentence(sentences: List[str]) -> str:
    # Create a new sentence from the last word of each sentence.
    last_words = extract_last_words(sentences)
    return " ".join(last_words).capitalize() + "."


def count_whitespaces(text: str) -> int:
    # Count all whitespace characters.
    return sum(1 for char in text if char.isspace())


def transform_text(text: str) -> str:
    # Full text transformation pipeline.
    fixed_text = fix_misspelling(text)
    sentences = split_into_sentences(fixed_text)
    normalized_sentences = normalize_sentences(sentences)
    extra_sentence = build_last_words_sentence(normalized_sentences)
    return " ".join(normalized_sentences) + " " + extra_sentence


def main() -> None:
    final_text = transform_text(TEXT)
    whitespace_count = count_whitespaces(TEXT)

    print("Normalized text:")
    print(final_text)
    print()
    print("Whitespace characters:", whitespace_count)


if __name__ == "__main__":
    main()
