<div align="center">
  <img src="gfx/logo_title.png" alt="Lingo Rush">
  <h2>A Multi-Language Translation Game By Joshua Sharpe</h2>
  <h2>LingoRush is an interactive application where players translate words or phrases into various languages, test their language skills, and progress through levels. Built with Python and Tkinter, it provides a fun way to learn new languages.</h2>
</div>

## Features
- **Tkinter Graphics**: A responsive and user-friendly GUI built with Python's Tkinter library.
-  **MyMemory Translation API**: Fetch accurate translations for words and phrases in multiple languages.
-  **RapidFuzz API**: Advanced similarity matching to evaluate user input.
- **Multiple languages supported**: English, French, Italian, Spanish, Russian, Portuguese, Chinese, and German.
---
## Files
- ```main.py``` Main script to create Tkinter instance
- ```gui.py``` Contains the graphical user interface (GUI) components and logic. Manages the layout, widgets, and user interactions for the game using Tkinter.
- ```utilities.py``` Includes helper functions and constants used throughout the application, such as translation logic, similarity evaluation, and pre-defined constants like supported languages and levels.
- ```wordlist.py``` Defines the word and phrase lists for the game, organized by difficulty levels (Level 1, Level 2, Level 3). These lists are used as the source for words to translate during gameplay.
- ```requirments.py``` A list of dependencies needed to install before running the application.

## Setup Instructions
Follow these steps to run the application on your local machine:

### Prerequisites
1. **Python 3.9-3.11** Ensure you have Python 3.9-3.11 installed on your system. If not, download it from [python.org](https://www.python.org/downloads/).
2. **Git**: Optionally, you can install Git to clone the repository ([Git Installation Guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)).

### Step 1: Download/Clone the Repository
Clone this repository to your local machine using:
```bash
git clone https://github.com/JosharpeTM/Multi-Language-Translator-Game
```
### Step 2: Navigate to the Project Directory
Change into the project directory:
```bash
cd [insert folder directory]
```
### Step 3: Install Dependencies
Install all required dependencies using pip and the requirements.txt file:
```bash
pip install -r requirements.txt
```
### Step 4: Run Application
Launch the game by running:
```bash
python main.py
```
---
## Dependencies
- ```regex```
- ```rapidfuzz```
- ```translate``` (MyMemory API)
- ```tkinter```
---

MIT License

Copyright (c) 2024 Joshua Sharpe

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the So
ftware, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.




