import os
import webbrowser

def manage_mods(game_path):
    mods_file_path = os.path.join(game_path, 'Mods', 'Mods.txt')
    
    if not os.path.exists(mods_file_path):
        return f"Mods.txt not found at: {mods_file_path}"

    # Attempt to open Mods.txt in the default text editor
    try:
        webbrowser.open(mods_file_path)
        return "Mods.txt opened in the default text editor. Make sure to save the file before exiting the editor."
    except Exception as e:
        return f"Error opening Mods.txt: {e}"
