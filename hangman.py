
import random

# Words used in the game
WORDS = [
    "PYTHON",
    "HANGMAN",
    "COMPUTER",
    "PROGRAMMING",
    "DEVELOPER",
    "KEYBOARD",
    "DATABASE",
    "ALGORITHM",
    "SOFTWARE",
    "TECHNOLOGY"
]

# ASCII art for each stage: 0 to 6 incorrect guesses
HANGMAN_STAGES = [
    """
     +---+
     |   |
         |
         |
         |
    ========
    """,
    """
     +---+
     |   |
     O   |
         |
         |
    ========
    """,
    """
     +---+
     |   |
     O   |
     |   |
         |
    ========
    """,
    """
     +---+
     |   |
     O   |
    /|   |
         |
    ========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
         |
    ========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
    ========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
    ========
    """
]


def display_word(secret_word, guessed_letters):
    """Display guessed letters and mask the remaining letters."""
    return " ".join(
        letter if letter in guessed_letters else "_"
        for letter in secret_word
    )


def play_hangman():
    secret_word = random.choice(WORDS)
    guessed_letters = set()
    incorrect_letters = set()
    max_attempts = 6

    print("=" * 35)
    print("       WELCOME TO HANGMAN!")
    print("=" * 35)
    print("Guess the hidden word one letter at a time.")
    print(f"You have {max_attempts} incorrect attempts.\n")

    while len(incorrect_letters) < max_attempts:
        mistakes = len(incorrect_letters)

        print(HANGMAN_STAGES[mistakes])
        print("Word:", display_word(secret_word, guessed_letters))
        print("Incorrect letters:",
              ", ".join(sorted(incorrect_letters)) or "None")
        print(f"Attempts remaining: {max_attempts - mistakes}")

        # Check whether all letters have been guessed
        if all(letter in guessed_letters for letter in secret_word):
            print("\nCongratulations! You guessed the word:",
                  secret_word)
            print("You won!")
            return

        guess = input("\nEnter a letter: ").strip().upper()

        # Validate input
        if len(guess) != 1 or not guess.isalpha() or not guess.isascii():
            print("Invalid input! Please enter one English letter.\n")
            continue

        # Prevent duplicate guesses
        if guess in guessed_letters or guess in incorrect_letters:
            print(f"You already guessed '{guess}'. Try another letter.\n")
            continue

        # Process the guess
        if guess in secret_word:
            guessed_letters.add(guess)
            print(f"Correct! '{guess}' is in the word.\n")
        else:
            incorrect_letters.add(guess)
            print(f"Wrong! '{guess}' is not in the word.\n")

    # Display the final stage after losing
    print(HANGMAN_STAGES[max_attempts])
    print("Word:", display_word(secret_word, guessed_letters))
    print("\nGame over! You ran out of attempts.")
    print("The correct word was:", secret_word)


if __name__ == "__main__":
    play_hangman()
