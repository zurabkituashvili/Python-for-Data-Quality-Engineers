from __future__ import annotations

import csv
import os
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = BASE_DIR / "news_feed.txt"
DEFAULT_INPUT_DIR = BASE_DIR / "input_records"
WORD_COUNT_FILE = BASE_DIR / "word-count.csv"
LETTER_STATS_FILE = BASE_DIR / "letter-count.csv"


class StatisticsBuilder:
    WORD_PATTERN = re.compile(r"[^\W\d_]+", flags=re.UNICODE)

    @classmethod
    def rebuild_csv_reports(
        cls,
        source_file: Path = OUTPUT_FILE,
        word_csv: Path = WORD_COUNT_FILE,
        letter_csv: Path = LETTER_STATS_FILE,
    ) -> None:
        text = source_file.read_text(encoding="utf-8") if source_file.exists() else ""
        cls._write_word_count_csv(text, word_csv)
        cls._write_letter_statistics_csv(text, letter_csv)

    @classmethod
    def _write_word_count_csv(cls, text: str, output_file: Path) -> None:
        words = [word.lower() for word in cls.WORD_PATTERN.findall(text)]
        word_counts = Counter(words)

        with output_file.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["word", "count"])
            for word, count in sorted(word_counts.items()):
                writer.writerow([word, count])

    @classmethod
    def _write_letter_statistics_csv(cls, text: str, output_file: Path) -> None:
        all_counts: defaultdict[str, int] = defaultdict(int)
        uppercase_counts: defaultdict[str, int] = defaultdict(int)

        for char in text:
            if char.isalpha():
                normalized = char.lower()
                all_counts[normalized] += 1
                if char.isupper():
                    uppercase_counts[normalized] += 1

        total_letters = sum(all_counts.values())

        with output_file.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["letter", "cout_all", "count_uppercase", "percentage"])

            for letter in sorted(all_counts):
                count_all = all_counts[letter]
                count_uppercase = uppercase_counts[letter]
                percentage = (
                    round((count_all / total_letters) * 100, 2) if total_letters else 0
                )
                writer.writerow([letter, count_all, count_uppercase, percentage])


class TextNormalizer:
    @staticmethod
    def normalize_text(text: str) -> str:
        text = re.sub(r"\biz\b", "is", text.strip(), flags=re.IGNORECASE)
        text = re.sub(r"\s+", " ", text)

        parts = re.split(r"([.!?])", text)
        sentences: List[str] = []

        for i in range(0, len(parts) - 1, 2):
            sentence = parts[i].strip()
            punctuation = parts[i + 1]

            if sentence:
                sentence = sentence.lower()
                sentence = sentence[0].upper() + sentence[1:]
                sentences.append(sentence + punctuation)

        if len(parts) % 2 == 1:
            tail = parts[-1].strip()
            if tail:
                tail = tail.lower()
                tail = tail[0].upper() + tail[1:]
                sentences.append(tail)

        return " ".join(sentences)

    @staticmethod
    def normalize_title(value: str) -> str:
        value = re.sub(r"\biz\b", "is", value.strip(), flags=re.IGNORECASE)
        value = re.sub(r"\s+", " ", value)
        return value.title()


class Record:
    def __init__(self, text: str) -> None:
        self.text = TextNormalizer.normalize_text(text)

    def publish(self) -> str:
        raise NotImplementedError("Subclasses must implement publish method")


class News(Record):
    def __init__(self, text: str, city: str) -> None:
        super().__init__(text)
        self.city = TextNormalizer.normalize_title(city)

    def publish(self) -> str:
        current_date = datetime.now().strftime("%d/%m/%Y %H:%M")
        return (
            "News\n"
            "-------------------------\n"
            f"{self.text}\n"
            f"{self.city}, {current_date}\n\n"
        )


class PrivateAd(Record):
    def __init__(self, text: str, expiration_date: str) -> None:
        super().__init__(text)
        self.expiration_date = expiration_date
        self._validated_expiration = datetime.strptime(expiration_date, "%d/%m/%Y")

    def publish(self) -> str:
        today = datetime.now()
        days_left = (self._validated_expiration - today).days

        return (
            "Private Ad\n"
            "-------------------------\n"
            f"{self.text}\n"
            f"Actual until: {self.expiration_date}, {days_left} days left\n\n"
        )


class JokeOfTheDay(Record):
    def __init__(self, text: str) -> None:
        super().__init__(text)

    def publish(self) -> str:
        funny_score = min(len(self.text) // 10, 10)

        return (
            "Joke of the Day\n"
            "-------------------------\n"
            f"{self.text}\n"
            f"Funny meter: {funny_score}/10\n\n"
        )


class FileRecordProvider:
    def __init__(self, default_folder: Path | str = DEFAULT_INPUT_DIR) -> None:
        self.default_folder = Path(default_folder)
        self.default_folder.mkdir(parents=True, exist_ok=True)

    def process(self, path: Optional[str] = None) -> int:
        target = Path(path) if path else self.default_folder

        if not target.exists():
            raise FileNotFoundError(f"Path does not exist: {target}")

        files = [target] if target.is_file() else sorted(target.glob("*.txt"))
        processed_files = 0

        for file_path in files:
            if self.process_file(file_path):
                processed_files += 1

        return processed_files

    def process_file(self, file_path: Path | str) -> bool:
        file_path = Path(file_path)

        try:
            records = self.parse_file(file_path)
            if not records:
                raise ValueError("No valid record blocks found")

            content = "".join(record.publish() for record in records)
            save_to_file(content)
            os.remove(file_path)
            print(f"Processed and removed file: {file_path}")
            return True
        except Exception as error:
            print(f"Failed to process '{file_path}': {error}")
            return False

    def parse_file(self, file_path: Path | str) -> List[Record]:
        raw_text = Path(file_path).read_text(encoding="utf-8")
        blocks = [
            block.strip()
            for block in re.split(r"\n\s*---\s*\n", raw_text)
            if block.strip()
        ]
        return [self.parse_block(block) for block in blocks]

    def parse_block(self, block: str) -> Record:
        data = {}

        for line in block.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                raise ValueError(f"Invalid line format: '{line}'. Expected key=value")

            key, value = line.split("=", 1)
            data[key.strip().lower()] = value.strip()

        record_type = data.get("type", "").lower()

        if record_type == "news":
            self._require_fields(data, ["text", "city"])
            return News(data["text"], data["city"])

        if record_type == "privatead":
            self._require_fields(data, ["text", "expiration_date"])
            return PrivateAd(data["text"], data["expiration_date"])

        if record_type in {"joke", "jokeoftheday"}:
            self._require_fields(data, ["text"])
            return JokeOfTheDay(data["text"])

        raise ValueError(f"Unsupported record type: '{record_type}'")

    @staticmethod
    def _require_fields(data: dict, fields: List[str]) -> None:
        missing = [field for field in fields if not data.get(field)]
        if missing:
            raise ValueError(f"Missing required field(s): {', '.join(missing)}")


def save_to_file(content: str, filename: Path | str = OUTPUT_FILE) -> None:
    filename = Path(filename)

    with filename.open("a", encoding="utf-8") as file:
        file.write(content)

    StatisticsBuilder.rebuild_csv_reports(source_file=filename)


def create_record_from_console() -> Optional[Record]:
    print("\nSelect what you want to add:")
    print("1 - News")
    print("2 - Private Ad")
    print("3 - Joke of the Day")
    print("4 - Process text file")
    print("0 - Exit")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        text = input("Enter news text: ")
        city = input("Enter city: ")
        return News(text, city)

    if choice == "2":
        text = input("Enter ad text: ")
        expiration_date = input("Enter expiration date (dd/mm/yyyy): ")
        return PrivateAd(text, expiration_date)

    if choice == "3":
        text = input("Enter your joke: ")
        return JokeOfTheDay(text)

    if choice == "4":
        provider = FileRecordProvider()
        path = input(
            f"Enter file or folder path (press Enter for default folder: {provider.default_folder}): "
        ).strip()
        processed = provider.process(path or None)
        print(f"Successfully processed {processed} file(s).")
        return None

    if choice == "0":
        raise SystemExit("Goodbye!")

    print("Invalid choice, try again.")
    return None


def main() -> None:
    print(f"Output file: {OUTPUT_FILE}")
    print(f"Default input folder for text files: {DEFAULT_INPUT_DIR}")

    StatisticsBuilder.rebuild_csv_reports()

    while True:
        try:
            record = create_record_from_console()
            if record is None:
                continue

            content = record.publish()
            save_to_file(content)
            print("Record added successfully! CSV reports recreated.")
        except SystemExit as exit_message:
            print(exit_message)
            break
        except Exception as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
