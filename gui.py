import random
import tkinter as tk
from tkinter import ttk
from utilities import translate, LEVELS, LANGUAGES, LANGUAGE_CODES, SIMILARITY_THRESHOLD
from rapidfuzz import fuzz

class TranslationGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Language Translation Game")
        self.apply_theme()

        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        self.score = 0
        self.level = 1
        self.lives = 5
        self.selected_language = None
        self.current_phrase = ""
        self.correct_translation = ""
        self.progress_bar = None

        self.setup_main_menu()

    def apply_theme(self):
        style = ttk.Style(self.root)
        style.theme_use('winnative')
        style.configure("TLabel", font=("Rockwell", 14), background="#f0f0f0", foreground="#333333")
        style.configure("TButton", font=("Rockwell", 14), background="#d9d9d9", foreground="#333333", padding=5, relief="flat", borderwidth=1)
        style.configure("TProgressbar", thickness=20)

    def setup_main_menu(self):
        self.clear_window()
        ttk.Label(self.root, text="Multi-Language Translation Game", font=("Rockwell", 20)).pack(pady=20)
        ttk.Button(self.root, text="Start Game", command=self.language_selection).pack(pady=10)
        ttk.Button(self.root, text="Rules", command=self.show_rules).pack(pady=10)
        ttk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)

    def show_rules(self):
        self.clear_window()
        ttk.Label(self.root, text="Game Rules", font=("Rockwell", 18)).pack(pady=10)
        ttk.Label(self.root, text="""Game Rules:
        1. Objective: Translate the given word or phrase into the selected language.
        2. Levels:
           - Level 1: Beginner words
           - Level 2: Simple phrases
           - Level 3: Intermediate phrases
        3. Scoring:
           - Level 1: 1 point per correct answer
           - Level 2: 2 points per correct answer
           - Level 3: 3 points per correct answer
        4. Level Progression:
           - 5 points to reach Level 2
           - 15 points to reach Level 3
           - 30 points to win the game
        5. Lives: Start with 5 lives. Incorrect answers lose 1 life.
        6. Game Over: Lose all lives or complete Level 3 to end the game.""", justify="left").pack(pady=10)
        ttk.Button(self.root, text="Back to Main Menu", command=self.setup_main_menu).pack(pady=10)

    def language_selection(self):
        self.clear_window()
        ttk.Label(self.root, text="Choose Language to Play", font=("Rockwell", 16)).pack(pady=20)
        for i, language in enumerate(LANGUAGES):
            ttk.Button(self.root, text=language, command=lambda i=i: self.start_game(i)).pack(pady=5)

    def start_game(self, language_index):
        self.selected_language = LANGUAGE_CODES[language_index]
        self.language_name = LANGUAGES[language_index]
        self.score = 0
        self.level = 1
        self.lives = 5
        self.main_game_loop()

    def main_game_loop(self):
        if self.lives == 0:
            self.display_message("Game Over", "You ran out of lives! Better luck next time.")
            self.setup_main_menu()
            return
        if self.level == 4:
            self.display_message("Congratulations!", "You completed the game. Well done!")
            self.setup_main_menu()
            return

        self.current_phrase = random.choice(list(LEVELS[self.level - 1]))
        self.correct_translation = translate(self.current_phrase, 'en', self.selected_language)

        self.clear_window()
        progress_frame = ttk.Frame(self.root)
        progress_frame.pack(pady=10)
        self.progress_bar = ttk.Progressbar(progress_frame, length=200, maximum=self.level_progress_target(), mode='determinate')
        self.progress_bar.pack(side=tk.LEFT, padx=5)
        self.update_progress_bar()

        ttk.Label(self.root, text=f"Score: {self.score}   Level: {self.level}   Lives: {self.lives}").pack(pady=10)
        ttk.Label(self.root, text=f"Translate the following word/phrase into {self.language_name}:").pack(pady=10)
        ttk.Label(self.root, text=f"{self.current_phrase}", font=("Rockwell", 18)).pack(pady=20)

        self.user_input = ttk.Entry(self.root)
        self.user_input.pack(pady=10)
        self.user_input.bind("<Return>", lambda event: self.check_answer())

        self.feedback_label = ttk.Label(self.root, text="")
        self.feedback_label.pack(pady=10)

        ttk.Button(self.root, text="Submit", command=self.check_answer).pack(pady=10)

    def check_answer(self):
        user_guess = self.user_input.get().strip().lower()
        similarity = fuzz.ratio(user_guess, self.correct_translation)

        if similarity >= SIMILARITY_THRESHOLD:
            self.score += self.level
            self.feedback_label.config(text="Correct!", foreground="green")
            if self.score >= self.level_progress_target():
                self.level += 1
                self.score = 0
                self.feedback_label.config(text=f"Great job! You've advanced to Level {self.level}!", foreground="green")
        else:
            self.lives -= 1
            self.feedback_label.config(text=f"Incorrect! The correct translation was: {self.correct_translation}", foreground="red")

        self.root.after(2000, self.main_game_loop)

    def level_progress_target(self):
        return {1: 5, 2: 10, 3: 15}.get(self.level, 0)

    def update_progress_bar(self):
        self.progress_bar['value'] = min(self.score, self.level_progress_target())

    def display_message(self, title, message):
        self.clear_window()
        ttk.Label(self.root, text=title, font=("Rockwell", 18)).pack(pady=10)
        ttk.Label(self.root, text=message).pack(pady=10)
        ttk.Button(self.root, text="Back to Main Menu", command=self.setup_main_menu).pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
