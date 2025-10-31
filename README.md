(Assignment Version)
# Hangman Game

## How to Run the Game
1. Open the `hangman_game` folder in Visual Studio Code.
2. Open the integrated terminal from the top menu: **View → Terminal**.
3. Run the game with the following command:
   ```bash
   python main.py


###  Follow the on-screen instructions:

Choose a category (Animals, Countries, Programming, Science, or type all to use all words)

Enter letters one at a time to guess the hidden word

Type guess to attempt the full word
Type quit to exit the game early
The player wins by guessing all letters correctly before using six wrong attempts.

####  Wordlist Format and Categories Used

##### The main word list is located in:

hangman_game/words/words.txt

This file must contain at least 1000 English words, each written on a separate line.
Example:
apple
banana
mountain
river
computer


######  Category files are stored inside:

hangman_game/words/categories/


The following categories are available:

animals.txt
countries.txt
programming.txt

science.txt
Each category file includes relevant words written in lowercase, one per line.

###### Scoring Method: 

The score for each game is calculated using the following formula:

Score = (Word length × 10) – (Wrong guesses × 5)


The player can make a maximum of 6 wrong guesses.
If the player wins, the earned score is added to the total score.
If the player loses, the score for that round is 0.

Overall statistics such as total score, games played, wins, losses, and win rate are automatically tracked and saved.

######  How Logs Are Saved

A new log folder is automatically created for every game session inside:

hangman_game/game_log/


Example:

game_log/game1/log.txt
game_log/game2/log.txt


Each log.txt file records:

Selected category and chosen word
All guesses made (correct and incorrect)
Number of wrong guesses
Final result (Win or Loss)
Score earned
Date and time of the game

Player statistics across all sessions are stored in:

hangman_game/game_log/stats.json

This file keeps a record of total games played, wins, losses, win rate, and average score per game.