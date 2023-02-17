"""Graphics for hangman.py

VERY INCOMPLETE!!!

TODO: make screens inherit from a base screen class
"""

import tkinter as tk

class HomeScreen():
    """Home screen"""
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Hangman")
        self.window.geometry("400x200")

        self.title = tk.Label(text="HANGMAN", font="Monaco 30")
        self.choice_label = tk.Label(text="How would you like to play?", font="Monaco 18")
        tk.Button(text="Computer guesses", bd=10, command=self.computer_guesses).place(x=30, y=110)
        tk.Button(text="User guesses", bd=10, command=self.user_guesses).place(x=230, y=110)

        self.title.pack(side=tk.TOP)
        self.choice_label.pack(side=tk.TOP)

        self.window.mainloop()

    def computer_guesses(self):
        """Computer guesses user's word"""
        print("Your turn to guess")
        self.window.destroy()
        self.compguess = ComputerGuessScreen()

    def user_guesses(self):
        """User guesses computer's word"""
        print("My turn to guess")
        self.window.destroy()

class ComputerGuessScreen():
    """Where the computer guesses the user's word"""
    user_word_length = 0

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Hangman: Computer guesses")
        self.window.geometry("400x200")

        self.title = tk.Label(text="How long is your word?", font="Monaco 25")
        self.entry = tk.Entry(font="Monaco 20", width=6, bd=4)
        self.submit = tk.Button(text="GO", font="Monaco", command=self.submit_length)

        self.title.pack(side=tk.TOP, pady=30)
        self.entry.place(x=140, y=130)
        self.submit.place(x=300,y=132)

        self.window.mainloop()

    def submit_length(self):
        """User submit's the length of their word"""
        print("Submit the length")
        user_input = self.entry.get()
        if user_input.isdigit() is True and int(user_input) < 10:
            self.user_word_length = int(user_input)
            self.window.destroy()
            print(self.user_word_length)
        else:
            self.window.destroy()
            ComputerGuessScreen()
        return self.user_word_length

class UserGuessScreen():
    """Where the user guesses the computer's word"""
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Hangman: Computer guesses")
        self.window.geometry("400x200")

if __name__ == "__main__":
    game = HomeScreen()
    print(game.compguess.user_word_length) # User word length
