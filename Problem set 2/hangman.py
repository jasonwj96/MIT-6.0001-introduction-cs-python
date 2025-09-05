# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
from string import ascii_lowercase

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print(len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word: str, letters_guessed: list[str]):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    return set(secret_word).issubset(letters_guessed)


def get_guessed_word(secret_word: str, letters_guessed: list[str]):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    return "".join([c if c in letters_guessed else "_" for c in secret_word])


def get_available_letters(letters_guessed: list[str]):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    return "".join(sorted(set(ascii_lowercase) - set(letters_guessed)))


def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    Starts up an interactive game of Hangman.
    '''
    guesses = 6
    warnings = 3
    letters_guessed = []

    print("Welcome to the game Hangman!")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")
    print("-" * 50)

    while guesses > 0:
        print(f"You have {guesses} guesses left.")
        print(f"Available letters: {get_available_letters(letters_guessed)}")

        guess = input("Please guess a letter: ").lower().strip()

        if len(guess) != 1 or guess not in ascii_lowercase:
            warnings -= 1
            if warnings < 0:
                guesses -= 1
                print(f"Invalid input! You lose one guess. Guesses left: {guesses}")
            else:
                print(f"Invalid input! You have {warnings} warnings left.")
            print("-" * 50)
            continue

        if guess in letters_guessed:
            warnings -= 1
            if warnings < 0:
                guesses -= 1
                print(f"Oops! Already guessed. You lose one guess. Guesses left: {guesses}")
            else:
                print(f"Oops! Already guessed. You have {warnings} warnings left.")
            print("-" * 50)
            continue

        letters_guessed.append(guess)

        if guess in secret_word:
            output = " ".join(get_guessed_word(secret_word, letters_guessed))
            print(f"Good guess: {output}")
        else:
            output = " ".join(get_guessed_word(secret_word, letters_guessed))
            print(f"Oops! That letter is not in my word: {output}")
            guesses -= 2 if guess in "aeiou" else 1

        print("-" * 50)

        if is_word_guessed(secret_word, letters_guessed):
            score = guesses * len(set(secret_word))
            print(f"Congratulations, you won! Your total score is: {score}")
            return

    print(f"Sorry, you ran out of guesses. The word was '{secret_word}'.")


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
# (hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean
    '''
    my_word = my_word.replace(" ", "")

    # Lengths must match
    if len(my_word) != len(other_word):
        return False

    for mw_char, ow_char in zip(my_word, other_word):
        if mw_char == "_":
            if ow_char in my_word:
                return False
        elif mw_char != ow_char:
            return False

    return True


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but prints out every word in wordlist that matches my_word
    '''
    matches = [word for word in wordlist if match_with_gaps(my_word, word)]

    if matches:
        print(" ".join(matches))
    else:
        print("No matches found")


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    Starts up an interactive game of Hangman with hints (*).
    '''
    guesses = 6
    warnings = 3
    letters_guessed = []

    print("Welcome to the game Hangman!")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")
    print("-" * 50)

    while guesses > 0:
        print(f"You have {guesses} guesses left.")
        print(f"Available letters: {get_available_letters(letters_guessed)}")

        guess = input("Please guess a letter (or * for a hint): ").lower().strip()

        if guess == "*":
            print("Possible word matches are:")
            show_possible_matches("".join(get_guessed_word(secret_word, letters_guessed)))
            print("-" * 50)
            continue

        if len(guess) != 1 or guess not in ascii_lowercase:
            warnings -= 1
            if warnings < 0:
                guesses -= 1
                print(f"Invalid input! You lose one guess. Guesses left: {guesses}")
            else:
                print(f"Invalid input! You have {warnings} warnings left.")
            print("-" * 50)
            continue

        if guess in letters_guessed:
            warnings -= 1
            if warnings < 0:
                guesses -= 1
                print(f"Oops! Already guessed. You lose one guess. Guesses left: {guesses}")
            else:
                print(f"Oops! Already guessed. You have {warnings} warnings left.")
            print("-" * 50)
            continue

        letters_guessed.append(guess)

        if guess in secret_word:
            output = " ".join(get_guessed_word(secret_word, letters_guessed))
            print(f"Good guess: {output}")
        else:
            output = " ".join(get_guessed_word(secret_word, letters_guessed))
            print(f"Oops! That letter is not in my word: {output}")
            guesses -= 2 if guess in "aeiou" else 1

        print("-" * 50)

        if is_word_guessed(secret_word, letters_guessed):
            score = guesses * len(set(secret_word))
            print(f"Congratulations, you won! Your total score is: {score}")
            return

    print(f"Sorry, you ran out of guesses. The word was '{secret_word}'.")


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.

    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

###############

# To test part 3 re-comment out the above lines and
# uncomment the following two lines.

secret_word = choose_word(wordlist)
hangman_with_hints(secret_word)
