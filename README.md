# Hangman
Two modes: computer chooses a word and the user guesses or the user chooses a word and the computer guesses. Current word length limit for user is 9 letters, soon to be increased. To be added is a difficulty setting.

This program uses letter frequencies and probabilities to guess the most likely letter to come next in a word. There are likely many better ways to for this to be implemented, but this is my first attempt at a program that is largely founded in math.

In the future, it might be nice to create a RNN that guesses the next possible letter for increased accuracy. 

# Usage
This is terminal text interface game. Tkinter graphics are pending.

# Bugs
There are many. For instance, if the program can't find any words that have follow the letter criteria, it cannot calculate the letter probabilities and make an informed guess. Instead, it tries to divide by zero, resulting in a crash. Feedback is always appreciated.
