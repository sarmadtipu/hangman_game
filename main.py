from pathlib import Path
from game.engine import HangmanCore
from game.wordlist import WordManager

def main():
    logs_folder = Path("game_log")

    word_manager = WordManager(Path("words/words.txt"))

    hangman = HangmanCore(word_manager, logs_folder)

    print("Welcome to Hangman!")
    categories = word_manager.get_categories()
    print("Available categories:", ", ".join(categories))
    category = input("Choose a category (type 'all' for every word): ").strip().lower()

    if category not in categories:
        print("Category not found. Using 'all'.")
        category = "all"

   
    hangman.launch(category)

if __name__ == "__main__":
    main()
