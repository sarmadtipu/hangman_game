from game.ascii_art import HANGMAN_PICS

class Display:
    def show_progress(self, progress, guessed, wrong_guesses, remaining):
        print("\nCurrent word: ", " ".join(progress))
        print("Guessed letters: ", ", ".join(sorted(guessed)))
        print(f"Wrong guesses: {wrong_guesses}  Remaining attempts: {remaining}")
        print(HANGMAN_PICS[wrong_guesses])

    def show_result(self, won, word, score, stats):
        print("\n=== Game Over ===")
        if won:
            print(f"Congratulations! You guessed the word: {word}")
            print(f"Score this round: {score}")
        else:
            print(f"You lost! The word was: {word}")
        print(f"Total games: {stats['games_played']} Wins: {stats['wins']} Losses: {stats['losses']}")
        print(f"Win rate: {stats['win_rate_str']}, Average score per game: {stats['avg_score']:.2f}")
