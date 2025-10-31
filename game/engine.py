import json
from pathlib import Path
from datetime import datetime
from ui.display import Display

class HangmanCore:
    """Handles gameplay, scoring, and logging."""

    def __init__(self, word_manager, logs_folder: Path):
        self.word_manager = word_manager
        self.logs_folder = Path(logs_folder)
        self.logs_folder.mkdir(parents=True, exist_ok=True)
        self.display = Display()
        self.max_attempts = 6
        self.stats_file = self.logs_folder / "stats.json"
        self.stats = self._load_stats()

    def _load_stats(self):
        """Load stats or create new."""
        if self.stats_file.exists():
            try:
                return json.loads(self.stats_file.read_text(encoding="utf-8"))
            except Exception:
                pass
        data = {"games_played": 0, "wins": 0, "losses": 0, "total_score": 0}
        self._save_stats(data)
        return data

    def _save_stats(self, data=None):
        """Save stats to file."""
        if data is None:
            data = self.stats
        gp = data.get("games_played", 0)
        wins = data.get("wins", 0)
        total = data.get("total_score", 0)
        data["win_rate"] = (wins / gp) if gp else 0.0
        data["win_rate_str"] = f"{data['win_rate']*100:.2f}%"
        data["avg_score"] = (total / gp) if gp else 0.0
        self.stats_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
        self.stats = data

    def _next_log_folder(self):
        n = 1
        while True:
            folder = self.logs_folder / f"game{n}"
            if not folder.exists():
                folder.mkdir(parents=True, exist_ok=False)
                return folder
            n += 1

    def _calculate_score(self, word, wrong):
        points = max(len(word) * 10 - wrong * 5, 0)
        return int(points)

    def launch(self, category="all"):
        word = self.word_manager.pick_random_word(category).lower()
        progress = ["_" for _ in word]
        guessed = set()
        wrong_guesses = 0

        # create log folder and file
        log_folder = self._next_log_folder()
        log_file = log_folder / "log.txt"

        with log_file.open("w", encoding="utf-8") as f:
            f.write(f"Game Log\nCategory: {category}\nWord: {word}\nLength: {len(word)}\n")
            f.write(f"Start Time: {datetime.now()}\n\n")

        while wrong_guesses < self.max_attempts and "_" in progress:
            remaining = self.max_attempts - wrong_guesses
            self.display.show_progress(progress, guessed, wrong_guesses, remaining)

            entry = input("Enter a letter (or 'guess' to guess full word, 'quit' to exit): ").strip().lower()

            if not entry:
                print("Input cannot be empty.")
                continue
            if entry == "quit":
                with log_file.open("a", encoding="utf-8") as f:
                    f.write("\nPlayer quit this game.\n")
                print("Game exited.")
                return
            if entry == "guess":
                full_guess = input("Enter your full word guess: ").strip().lower()
                if not full_guess.isalpha():
                    print("Word guesses must be letters only.")
                    continue
                if full_guess == word:
                    progress = list(word)
                    with log_file.open("a", encoding="utf-8") as f:
                        f.write(f"Full-word guess '{full_guess}' -> Correct\n")
                    break
                else:
                    wrong_guesses += 1
                    with log_file.open("a", encoding="utf-8") as f:
                        f.write(f"Full-word guess '{full_guess}' -> Wrong\n")
                    print("Incorrect full-word guess. +1 mistake.")
                    continue
            if len(entry) != 1 or not entry.isalpha():
                print("Enter a single letter.")
                continue
            if entry in guessed:
                print("Letter already tried. No penalty.")
                continue

            guessed.add(entry)
            if entry in word:
                for i, c in enumerate(word):
                    if c == entry:
                        progress[i] = entry
                with log_file.open("a", encoding="utf-8") as f:
                    f.write(f"Letter '{entry}' -> Correct\n")
                print("Correct!")
            else:
                wrong_guesses += 1
                with log_file.open("a", encoding="utf-8") as f:
                    f.write(f"Letter '{entry}' -> Wrong\n")
                print("Wrong!")

        won = "_" not in progress
        score = self._calculate_score(word, wrong_guesses) if won else 0

        # Update stats
        self.stats["games_played"] += 1
        if won:
            self.stats["wins"] += 1
        else:
            self.stats["losses"] += 1
        self.stats["total_score"] += score
        self._save_stats()

        with log_file.open("a", encoding="utf-8") as f:
            f.write("\nSummary\n")
            f.write(f"Wrong guesses: {wrong_guesses}\n")
            f.write(f"Result: {'Win' if won else 'Loss'}\n")
            f.write(f"Score: {score}\n")
            f.write(f"Date & Time: {datetime.now()}\n")

        self.display.show_result(won, word, score, self.stats)
