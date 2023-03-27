"""
Hangman game

Intended Functionality:
  •  Mode 1: computer picks a word, user guesses
  •  Mode 2: user picks a word, computer guesses

TODO: Create character-level RNN to guess next letter
TODO: Add Tkinter display
TODO: Optimize word sorting with regex
"""

import collections
import os
import random as r
import sys
import requests

os.system("clear")

# If for some reason the data download is not working, it is best to import the text file

## Open words text file
#try:
#    # Contains around 58,000 words
#    with open("data/common_words.txt", "r", encoding="utf-8") as f:
#        words = [word.replace('\n', '') for word in f.readlines()]
#except Exception as exc:
#    raise IOError("Exception occured when reading file") from exc

# If you are importing the words list from text file, comment out the following try-except block

try:
    data = requests.get("http://www.mieliestronk.com/corncob_lowercase.txt", timeout=10)
    words = data.text.split('\r\n')
except Exception as exc:
    print("Could not get words list. Import words from text file")
    sys.exit(1)

def letter_probability(letter: str,
                       required_letters_in_word: list,
                       forbidden_letters: list,
                       length: int):
    """
    Calculate the probability that a given letter will appear in a string of given length
    letter -- letter to calculate probability of
    required_letters_in_word -- letters that must be present in a word to be considered.
                             -- leave as [''] for no specific letters.
    """

    # Properly format lists
    if not required_letters_in_word:
        required_letters_in_word = ['']
    if not forbidden_letters:
        forbidden_letters = ['']
    choice_words = []

    avg_freq_per_word = 0

    # TODO: search for words with letters in the correct position instead of
    #       just words that contain the correct letters
    # TODO: maybe find a way to do this with a regex?

    # Filter out words that do not fit the requirements
    for i, word in enumerate(words):
        if len(word) == length:
            s = 0 # number of letters present in the provided list of letters
            for char in required_letters_in_word:
                if char in word:
                    s += 1
            if s == len(required_letters_in_word):
                f_s = 0 # number of letters present in the list of forbidden letters
                for char in word:
                    if char in forbidden_letters:
                        f_s += 1
                if f_s == 0:
                    choice_words.append(word) # add current word to list of acceptale words

    # Get the frequency of every letter in a word
    for i, word in enumerate(choice_words):
        # d is a collection of the frequencies of each letter in a word
        d = collections.defaultdict(int)
        for char in word:
            d[char] += 1
        # add the frequency of the user specified letter to the average freq. variable
        # avg_freq_per_word is mutated later to reflect the true average letter frequency
        avg_freq_per_word += d[letter]

    avg_freq_per_word /= len(choice_words)
    return avg_freq_per_word

def most_probable_letters(required_letters_in_word: list,
                          forbidden_letters: list,
                          length: int):
    """
    Given a set of letters, return a list of the most popular letters present 
    in words of a specific length.
    """
    letters_dict = {}
    # loop through the letters of the alphabet
    for i in range(97, 123):
        # add the current letter in the loop and its probability in the word to the dictionary
        # in the format:    { letter: probability }
        letters_dict.update({chr(i): letter_probability(chr(i),
                                                        required_letters_in_word,
                                                        forbidden_letters,
                                                        length
                                                        )})
    # return the reversed list of probabilities
    return [i for i in reversed(list({k: v for k, v in sorted(letters_dict.items(),
                                                              key=lambda item: item[1])}.keys()))]

def pick_random_word(length: int):
    """Pick a random word of certain length"""
    choice_words = []
    for i, word in enumerate(words):
        if len(word) == length:
            choice_words.append(word)
    return r.choice(choice_words)

def gameplay_usr_guesses():
    """Gameplay for when user guesses the word picked by the computer"""
    guesses_remaining = 10
    incorrect_letter_guesses = []
    correct_letter_guesses = []
    guessing_word = pick_random_word(r.randint(4, 6))
    # print(guessing_word)

    while guesses_remaining > 0:
        os.system('clear')
        display_str = ""

        # Display the  letters guessed and not guessed
        for char in guessing_word:
            if char in correct_letter_guesses:
                display_str += f" {char}"
            else:
                display_str += ' _'

        # Check if the user has won
        if list(set(display_str.replace(' ', ''))) == correct_letter_guesses:
            print("\nCongrats! You won!\n")
            sys.exit(1)

        print(f"\nYou have {guesses_remaining} tries to guess the {len(guessing_word)}-letter word")
        print(f"\t\t{display_str}\n")
        #print(most_probable_letters(correct_letter_guesses, len(guessing_word)))
        print(f"Correct guesses: {correct_letter_guesses}")
        print(f"Incorrect guesses: {incorrect_letter_guesses}")
        letter_guess = input("Guess one letter: ")

        # exit the game
        if letter_guess == 'exit':
            print(f"\nThe correct word was \033[1m\033[3m{guessing_word}\033[0m\n")
            sys.exit(1)
        if letter_guess in guessing_word:
            # if the letter is present in the computer's word...
            correct_letter_guesses.append(letter_guess)
            guesses_remaining += 1
        else:
            incorrect_letter_guesses.append(letter_guess)

        letter_guess = letter_guess[0] # just in case the user inputs more than one letter
        correct_letter_guesses = list(set(correct_letter_guesses))
        incorrect_letter_guesses = list(set(incorrect_letter_guesses))
        guesses_remaining -= 1

    print("\nYou lost! Better luck next time!")
    print(f"The word was \033[1m\033[3m{guessing_word}\033[0m.\n")
    next_choice = input("Would you like to play again (y/n)? ")

    if next_choice.lower() == "y":
        os.system("clear")
        main()
    else:
        sys.exit(1)

def gameplay_comp_guesses():
    """Gameplay for when computer guesses the word picked by the user"""
    os.system('clear')
    correct_letters = []
    incorrect_letters = []

    word_length = int(input("How long is your word? "))
    if word_length >= 10:
        gameplay_comp_guesses()

    word = ["_" for i in range(word_length)]

    guesses_remaining = 10

    while guesses_remaining > 0:
        os.system('clear')
        guess_ix = 0
        guesses = most_probable_letters(correct_letters, incorrect_letters, word_length)
        guess = guesses[guess_ix]

        display_str = ' '.join(word)

        while guess in correct_letters:
            guess_ix += 1
            guess = guesses[guess_ix]

        print(f"\nI have {guesses_remaining} tries to guess the {word_length}-letter word\n")
        print(f"Word so far: {display_str}")
        print(" " * 13 + ' '.join([str(i+1) for i in range(word_length)]))
        print(f"Where does the letter \033[95m\033[1m{guess}\033[0m appear in your word?")
        print("(0 if it does not, separate positions by commas if there are multiple)")
        feedback = input("Pos: ")
        feedback = feedback.replace(' ', '')

        if feedback == "exit":
            print("Exiting...")
            sys.exit(1)

        # This following block formats the user's feedback and checks
        # Additionally, check if the computer is correct or not
        if ',' in feedback:
            feedback = feedback.split(',')
        else:
            feedback = list(feedback)
        for i, elem in enumerate(feedback):
            feedback[i] = int(elem)

        if feedback[0] > 0:
            for i in feedback:
                word[i-1] = f"\033[4m{guess}\033[0m"
                correct_letters.append(guess)
            guesses_remaining += 1
        else:
            incorrect_letters.append(guess)
        if len(correct_letters) == word_length:
            print(f"\nYay! I won!\nThe word was {''.join(word)}\033[0m\n")

            next_choice = input("Would you like to play again (y/n)? ")
            if next_choice.lower() == "y":
                os.system("clear")
                main()
            else:
                sys.exit(1)
        guesses_remaining -= 1
        if guesses_remaining == 0:
            print("\nAww, I lost! :(")
            n = input("Would you like me to keep guessing? (y/n) ")
            if n == 'y':
                guesses_remaining += 10
            else:
                input("\nWhat was the word? ")
                next_choice = input("\nThanks for playing! Would you like to play again (y/n)? ")
                if next_choice.lower() == "y":
                    os.system("clear")
                    main()
                else:
                    sys.exit(1)

def main():
    """Main functionality. Allows user to restart if they wish"""
    print("How would you like to play?")
    print("\nOption 1: Computer guesses your word")
    print("Option 2: You guess the computer's word")
    choice = input("1 or 2: ")
    if choice == "1":
        gameplay_comp_guesses()
    if choice == "2":
        gameplay_usr_guesses()
    else:
        os.system("clear")
        print("Please enter 1 or 2")
        main()

if __name__ == "__main__":
    main()
