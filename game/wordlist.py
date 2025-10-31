import random
from pathlib import Path

class WordManager:
    def __init__(self, word_file: Path):
        self.word_file = Path(word_file)
        if not self.word_file.exists():
            raise ValueError("words.txt file not found!")
        self.words = self._load_words()

    def _load_words(self):
        """Load all words into a list"""
        with self.word_file.open("r", encoding="utf-8") as f:
            words = [line.strip() for line in f if line.strip()]
        if not words:
            raise ValueError("words.txt is empty!")
        return words

    def pick_random_word(self, category="all"):
        # For simplicity, 'category' ignored here; can expand later
        return random.choice(self.words)

    def get_categories(self):
        return ["all", "animals", "countries", "programming", "science"]
