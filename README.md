# CAT RATER
Python app with Tkinter GUI.

It uses [The Cat API](https://thecatapi.com/) to fetch and display cat pictures. Then prompts the user to rate them 1-5 stars 

Each rating is then stored in an SQLite3 database.

- Windows path: `%LOCALAPPDATA%/CatRater`
- Linux/macOS path: `home/.catrater`

The database entries are used for avoiding duplicate cat pictures.

## HOW TO USE?
Simple, just click a start depending on the rating you would like to give to each cat picture

## HOW TO INSTALL?
### COOL DEVELOPER MODE
1. `python -m venv .venv` To create a virtual enviroment to download dependencies  
2. `.venv/Scripts/active` To access the .venv  
3. `pip install -r requirements.txt` To install all necessary dependencies

### WINDOWS USER MODE
 1. `main.exe` Just double click the executable lol (You can get this in the releases page in the repo)

I don't haven't tried if it works on Linux, you're free to try it.

