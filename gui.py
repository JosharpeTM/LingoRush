import random
import tkinter as tk
from tkinter import ttk
from utilities import translate, LEVELS, LANGUAGES, LANGUAGE_CODES, SIMILARITY_THRESHOLD
from rapidfuzz import fuzz

class TranslationGame:
    def __init__(self, root):
        #Initialize frame
        self.root = root
        self.root.title("Multi-Language Translation Game")
        self.apply_theme()

        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        #Initialize game variables
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
        ttk.Button(self.root, text="Translate", command=self.translation_app).pack(pady=10)
        ttk.Button(self.root, text="Rules", command=self.show_rules).pack(pady=10)
        ttk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)

    def translation_app(self):
        self.clear_window()
        
        ttk.Label(self.root, text="Translation Tool", font=("Rockwell", 18)).pack(pady=20)

        # Dropdown menu for selecting the source language
        source_frame = ttk.Frame(self.root)
        source_frame.pack(pady=10)
        ttk.Label(source_frame, text="Source Language:").grid(row=0, column=0, padx=10, pady=5)
        
        self.source_language = tk.StringVar(value=LANGUAGES[0])
        source_dropdown = ttk.Combobox(source_frame, textvariable=self.source_language, values=LANGUAGES, state="readonly")
        source_dropdown.grid(row=0, column=1, padx=10, pady=5)

        # Dropdown menu for selecting the target language
        target_frame = ttk.Frame(self.root)
        target_frame.pack(pady=10)
        ttk.Label(target_frame, text="Target Language:").grid(row=0, column=0, padx=10, pady=5)

        self.target_language = tk.StringVar(value=LANGUAGES[1])
        target_dropdown = ttk.Combobox(target_frame, textvariable=self.target_language, values=LANGUAGES, state="readonly")
        target_dropdown.grid(row=0, column=1, padx=10, pady=5)

        # Input box for the word/phrase to translate
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=10)
        ttk.Label(input_frame, text="Enter Text:").grid(row=0, column=0, padx=10, pady=5)
        
        self.word_to_translate = tk.StringVar()
        input_box = ttk.Entry(input_frame, textvariable=self.word_to_translate, width=100)
        input_box.grid(row=0, column=1, padx=10, pady=5)

        # Output box for the translated word/phrase
        output_frame = ttk.Frame(self.root)
        output_frame.pack(pady=10)
        ttk.Label(output_frame, text="Translation:").grid(row=0, column=0, padx=10, pady=5)
        
        self.translation_result = tk.StringVar()
        output_box = ttk.Entry(output_frame, textvariable=self.translation_result, width=100, state="readonly")
        output_box.grid(row=0, column=1, padx=10, pady=5)

        # Translate button
        ttk.Button(self.root, text="Translate", command=self.perform_translation).pack(pady=20)

        # Back to main menu button
        ttk.Button(self.root, text="Back to Main Menu", command=self.setup_main_menu).pack(pady=10)

    def perform_translation(self):
        source_language_code = LANGUAGE_CODES[LANGUAGES.index(self.source_language.get())]
        target_language_code = LANGUAGE_CODES[LANGUAGES.index(self.target_language.get())]
        text = self.word_to_translate.get().strip()

        if text:
            translated_text = translate(text, source_language_code, target_language_code)
            self.translation_result.set(translated_text)
        else:
            self.translation_result.set("Enter valid text!")

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
        self.progress_bar = ttk.Progressbar(progress_frame, length=400, maximum=self.level_progress_target(), mode='determinate')
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

        button_frame = ttk.Frame(self.root)
        button_frame.pack(expand=True, anchor=tk.CENTER)

        ttk.Button(button_frame, text="Submit", command=self.check_answer).pack(side=tk.LEFT, padx=5, anchor=tk.CENTER)
        ttk.Button(button_frame, text="Quit Game", command=self.setup_main_menu).pack(side=tk.LEFT, padx=5, anchor=tk.CENTER)

    def check_answer(self):
        user_guess = self.user_input.get().strip().lower()
        similarity = fuzz.ratio(user_guess, self.correct_translation)

        if similarity >= SIMILARITY_THRESHOLD:
            self.score += self.level
            self.feedback_label.config(text="Correct!", foreground="green")
            if self.score >= self.level_progress_target():
                self.level += 1
                self.score = 0
                self.feedback_label.config(text=f"Great job! You've advanced to Level {self.level}!", foreground="blue")
        else:
            self.lives -= 1
            self.feedback_label.config(text=f"Incorrect! The correct translation was: {self.correct_translation}", foreground="red", wraplength=400)

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
