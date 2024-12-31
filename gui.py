import random
import tkinter as tk
from tkinter import ttk
from utilities import translate, LEVELS, LANGUAGES, LANGUAGE_CODES, SIMILARITY_THRESHOLD
from rapidfuzz import fuzz

class TranslationGame:
    def __init__(self, root):
        # Initialize the main game window and apply UI settings
        self.root = root
        self.root.title("Multi-Language Translation Game")
        self.apply_theme()

        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # Initialize game variables
        self.score = 0
        self.level = 1
        self.lives = 5
        self.to_language = None
        self.english_phrase = ""
        self.source_translation = ""
        self.correct_translation = ""
        self.progress_bar = None

        self.setup_main_menu()

    def apply_theme(self):
        # Apply a consistent theme to the UI elements
        style = ttk.Style(self.root)
        style.theme_use('xpnative')
        style.configure("TLabel", font=("Rockwell", 14), background="#f0f0f0", foreground="#333333")
        style.configure("TButton", font=("Rockwell", 14), background="#d9d9d9", foreground="#333333", padding=5, relief="flat", borderwidth=1)
        style.configure("TProgressbar", thickness=20)

    def setup_main_menu(self):
        # Create the main menu interface
        self.clear_window()

        try:
            # Load logo image for the main menu
            self.logo_image = tk.PhotoImage(file="gfx/logo_title.png")
        except Exception as e:
            print(f"Error loading image: {e}")
            self.logo_image = None

        # Display the logo or fallback title
        if self.logo_image:
            logo_label = ttk.Label(self.root, image=self.logo_image)
            logo_label.pack(pady=20)
        else:
            ttk.Label(self.root, text="LINGO RUSH", font=("Rockwell", 20)).pack(pady=20)

        # Add menu buttons
        ttk.Label(self.root, text="A Multi-Language Translation Game By Joshua Sharpe", font=("Rockwell", 20)).pack(pady=20)
        ttk.Button(self.root, text="Start Game", command=self.language_selection).pack(pady=10)
        ttk.Button(self.root, text="Translate", command=self.translation_app).pack(pady=10)
        ttk.Button(self.root, text="Rules", command=self.show_rules).pack(pady=10)
        ttk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)

    def translation_app(self):
        # Set up the translation tool interface
        self.clear_window()
        
        ttk.Label(self.root, text="Translation Tool", font=("Rockwell", 18)).pack(pady=20)

        # Dropdown menu for source language selection
        source_frame = ttk.Frame(self.root)
        source_frame.pack(pady=10)
        ttk.Label(source_frame, text="Source Language:").grid(row=0, column=0, padx=10, pady=5)
        
        self.source_language = tk.StringVar(value=LANGUAGES[0])
        source_dropdown = ttk.Combobox(source_frame, textvariable=self.source_language, values=LANGUAGES, state="readonly")
        source_dropdown.grid(row=0, column=1, padx=10, pady=5)

        # Dropdown menu for target language selection
        target_frame = ttk.Frame(self.root)
        target_frame.pack(pady=10)
        ttk.Label(target_frame, text="Target Language:").grid(row=0, column=0, padx=10, pady=5)

        self.target_language = tk.StringVar(value=LANGUAGES[1])
        target_dropdown = ttk.Combobox(target_frame, textvariable=self.target_language, values=LANGUAGES, state="readonly")
        target_dropdown.grid(row=0, column=1, padx=10, pady=5)

        # Input box for text to translate
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=10)
        ttk.Label(input_frame, text="Enter Text:").grid(row=0, column=0, padx=10, pady=5)
        
        self.word_to_translate = tk.StringVar()
        input_box = ttk.Entry(input_frame, textvariable=self.word_to_translate, width=100)
        input_box.grid(row=0, column=1, padx=10, pady=5)

        # Output box for the translated text
        output_frame = ttk.Frame(self.root)
        output_frame.pack(pady=10)
        ttk.Label(output_frame, text="Translation:").grid(row=0, column=0, padx=10, pady=5)
        
        self.translation_result = tk.StringVar()
        output_box = ttk.Entry(output_frame, textvariable=self.translation_result, width=100, state="readonly")
        output_box.grid(row=0, column=1, padx=10, pady=5)

        ttk.Button(self.root, text="Translate", command=self.perform_translation).pack(pady=20)
        ttk.Button(self.root, text="Back to Main Menu", command=self.setup_main_menu).pack(pady=10)

    def perform_translation(self):
        # Perform translation using the selected languages and input text
        source_language_code = LANGUAGE_CODES[LANGUAGES.index(self.source_language.get())]
        target_language_code = LANGUAGE_CODES[LANGUAGES.index(self.target_language.get())]
        text = self.word_to_translate.get().strip()

        if text:
            translated_text = translate(text, source_language_code, target_language_code)
            self.translation_result.set(translated_text)
        else:
            self.translation_result.set("Enter valid text!")

    def show_rules(self):
        # Display game rules in a formatted interface
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
        # Allow the player to select source and target languages for the game
        self.clear_window()
        ttk.Label(self.root, text="Choose Source and Target Languages", font=("Rockwell", 16)).pack(pady=20)

        # Dropdown for source language
        source_frame = ttk.Frame(self.root)
        source_frame.pack(pady=10)
        ttk.Label(source_frame, text="Source Language:").grid(row=0, column=0, padx=10, pady=5)

        self.source_language = tk.StringVar(value=LANGUAGES[0])
        source_dropdown = ttk.Combobox(source_frame, textvariable=self.source_language, values=LANGUAGES, state="readonly")
        source_dropdown.grid(row=0, column=1, padx=10, pady=5)

        # Dropdown for target language
        target_frame = ttk.Frame(self.root)
        target_frame.pack(pady=10)
        ttk.Label(target_frame, text="Target Language:").grid(row=0, column=0, padx=10, pady=5)

        self.target_language = tk.StringVar(value=LANGUAGES[1])
        target_dropdown = ttk.Combobox(target_frame, textvariable=self.target_language, values=LANGUAGES, state="readonly")
        target_dropdown.grid(row=0, column=1, padx=10, pady=5)

        ttk.Button(self.root, text="Begin Game", command=self.start_game).pack(pady=20)
        ttk.Button(self.root, text="Back to Main Menu", command=self.setup_main_menu).pack(pady=10)

    def start_game(self):
        # Initialize game settings and begin the main loop
        self.from_language = LANGUAGE_CODES[LANGUAGES.index(self.source_language.get())]
        self.to_language = LANGUAGE_CODES[LANGUAGES.index(self.target_language.get())]
        self.score = 0
        self.level = 1
        self.lives = 5
        self.main_game_loop()

    def main_game_loop(self):
        # Core gameplay loop, handles level progression and user input
        if self.lives == 0:
            self.display_message("Game Over", "You ran out of lives! Better luck next time.")
            self.setup_main_menu()
            return
        if self.level == 4:
            self.display_message("Congratulations!", "You completed the game. Well done!")
            self.setup_main_menu()
            return

        # Select a random phrase and generate translations
        self.english_phrase = random.choice(list(LEVELS[self.level - 1]))
        self.source_translation = translate(self.english_phrase, 'en', self.from_language)
        self.correct_translation = translate(self.source_translation, self.from_language, self.to_language)

        self.clear_window()

        # Set background to an image representing the target language
        try:
            self.bg_image = tk.PhotoImage(file=f"gfx/language/{self.target_language.get()}.png")
        except Exception as e:
            print(f"Error loading background image: {e}")
            self.bg_image = None

        if self.bg_image:
            bg_label = tk.Label(self.root, image=self.bg_image)
            bg_label.place(relwidth=1, relheight=1)
        
        # Display progress and game details
        progress_frame = ttk.Frame(self.root)
        progress_frame.pack(pady=10)
        self.progress_bar = ttk.Progressbar(progress_frame, length=400, maximum=self.level_progress_target(), mode='determinate')
        self.progress_bar.pack(side=tk.LEFT, padx=5)
        self.update_progress_bar()

        ttk.Label(self.root, text=f"Score: {self.score}   Level: {self.level}   Lives: {self.lives}").pack(pady=10)
        ttk.Label(self.root, text=f"Translate the following word/phrase into {self.target_language.get()}:").pack(pady=10)
        ttk.Label(self.root, text=f"{self.source_translation}", font=("Rockwell", 18)).pack(pady=20)

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
        # Check the user's answer for similarity and provide feedback
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
        # Remove all widgets from the window to prepare for a new screen
        for widget in self.root.winfo_children():
            widget.destroy()
