from pynput import keyboard
import time
import re
import psutil  # For CPU usage details
import tkinter as tk  # For GUI overlay
from threading import Thread

# Global variables
valid_lines_count = 0  # Counter for valid lines of code
session_start = time.time()
current_line = ""  # Store current line before Enter

# Enhanced regular expression to match more types of code lines
code_pattern = re.compile(
    r'(int|float|double|char|bool|void|def|function|class|interface|enum|struct|console\.log|#include|#define|#ifdef|#ifndef|std::|return|import|from|export|let|const|var|public|private|protected|static|final|new|delete|throw|try|catch|finally|for|while|do|if|else|switch|case|break|continue|print|println|cout|cin|printf|scanf|lambda|=>|\b\w+\s*=\s*.+)\b'
)

# Termination string
TERMINATION_STR = 'stop_track'
termination_buffer = ""  # Buffer to track the termination string

# Create a Tkinter overlay window
root = tk.Tk()
root.title("Code Line Counter")
root.attributes("-topmost", True)  # Always on top
root.overrideredirect(True)  # Remove window decorations
root.geometry("200x100+10+10")  # Set window size and position (x, y)

# Variables for window movement
start_x = 0
start_y = 0

def move_window(event):
    """Move the window when dragged."""
    x = root.winfo_pointerx() - start_x
    y = root.winfo_pointery() - start_y
    root.geometry(f"+{x}+{y}")

def start_move(event):
    """Start moving the window."""
    global start_x, start_y
    start_x = root.winfo_pointerx() - root.winfo_rootx()
    start_y = root.winfo_pointery() - root.winfo_rooty()

def minimize_window():
    """Minimize the window."""
    root.attributes("-topmost", False)  # Disable "always on top" temporarily
    root.iconify()  # Minimize the window
    root.attributes("-topmost", True)  # Re-enable "always on top"

def close_window():
    """Close the window and terminate the program."""
    display_summary_and_exit()

# Toolbar frame for minimize and close buttons
toolbar = tk.Frame(root, bg="gray")
toolbar.pack(fill=tk.X)

# Minimize button
minimize_button = tk.Button(toolbar, text="-", command=minimize_window, bg="gray", fg="white", bd=0)
minimize_button.pack(side=tk.LEFT, padx=2)

# Close button
close_button = tk.Button(toolbar, text="x", command=close_window, bg="gray", fg="white", bd=0)
close_button.pack(side=tk.RIGHT, padx=2)

# Label to display the count and CPU usage
count_label = tk.Label(root, text="Valid Lines: 0\nCPU Usage: 0%", font=("Arial", 12))
count_label.pack(pady=10)

# Bind mouse events to move the window
toolbar.bind("<ButtonPress-1>", start_move)
toolbar.bind("<B1-Motion>", move_window)

def update_overlay():
    """Update the overlay with the current count of valid lines and CPU usage."""
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)  # Get CPU usage
        count_label.config(text=f"Valid Lines: {valid_lines_count}\nCPU Usage: {cpu_usage}%")
        time.sleep(1)  # Update every second

def on_press(key):
    global current_line, termination_buffer

    try:
        if hasattr(key, 'char') and key.char:  
            current_line += key.char  # Append typed characters
            termination_buffer += key.char  # Append to termination buffer

            # Check if the termination string is typed
            if TERMINATION_STR in termination_buffer:
                display_summary_and_exit()

        elif key == keyboard.Key.space:
            current_line += " "  # Add spaces to the current line
            termination_buffer += " "  # Add spaces to the termination buffer

        # Handle Backspace and Delete keys
        elif key == keyboard.Key.backspace:
            if current_line:  # Remove the last character
                current_line = current_line[:-1]
                termination_buffer = termination_buffer[:-1]

        elif key == keyboard.Key.delete:
            # Delete key doesn't modify `current_line` directly, so we ignore it
            pass

    except AttributeError:
        pass  # Ignore function keys

def on_release(key):
    global current_line, valid_lines_count

    if key == keyboard.Key.enter:
        stripped_line = current_line.strip()
        if stripped_line:  # Only count non-empty lines
            if code_pattern.search(stripped_line):  # Check if it's a line of code
                valid_lines_count += 1  # Increment the valid lines counter
                print(f"Valid lines coded: {valid_lines_count}")

        current_line = ""  # Reset current line

def display_summary_and_exit():
    """Display summary of lines coded and CPU usage, then exit."""
    elapsed_time = round(time.time() - session_start, 2)
    cpu_usage = psutil.cpu_percent(interval=1)  # Get CPU usage

    print("\n=== Session Summary ===")
    print(f"Valid lines coded: {valid_lines_count}")
    print(f"Time elapsed: {elapsed_time} sec")
    print(f"CPU Usage: {cpu_usage}%")

    print("\nProgram terminated.")
    root.destroy()  # Close the overlay window
    exit()

# Start the Tkinter overlay in a separate thread
overlay_thread = Thread(target=update_overlay, daemon=True)
overlay_thread.start()

# Start the keyboard listener in a separate thread
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

print(f"Program running in the background. Type '{TERMINATION_STR}' to terminate.")

# Start the Tkinter main loop
root.mainloop()