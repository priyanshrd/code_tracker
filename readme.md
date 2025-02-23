# Code Line Tracker

A Python tool to track valid lines of code in real-time. Displays an always-on-top overlay with line count and CPU usage. Logs code and session summaries. Move, minimize, or close the overlay. Terminate by typing `stop_track`.

---

## Features

- **Real-Time Tracking**: Tracks valid lines of code as you type.
- **Overlay Display**: Shows line count and CPU usage in an always-on-top window.
- **Movable Window**: Drag the overlay to any location.
- **Minimize and Close Buttons**: Minimize or terminate the program.
- **Logging**: Saves valid lines and session summaries to a file.

---

## Setup

### Prerequisites

- Python 3.x
- Libraries: `pynput`, `psutil`

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/priyanshrd/code_tracker.git
   cd code_tracker
   ```
Install the required libraries:

```bash
pip install pynput psutil
```
Run the script:

```bash
python code_line_tracker.py
```
Usage
Run the Program:

A small overlay window will appear, showing the line count and CPU usage.

Move the Overlay:

Click and hold the toolbar to drag it.

Minimize the Overlay:

Click the - button to minimize.

Close the Program:

Click the x button to terminate.

Terminate with a String:

Type stop_track to terminate.

Log Files
coding_progress.txt:

Logs valid lines with timestamps and session summaries.

lines_count.txt:

Saves the current count of valid lines.

Customization
Modify the Regular Expression
Edit the code_pattern variable to match specific programming constructs.

Change the Termination String
Modify the TERMINATION_STR variable to change the termination string.

Additions Accepted
Contributions are welcome! Ideas for improvements:

Support for More Languages: Add regex for additional languages.

Customizable Overlay: Allow font size and color changes.

Advanced Logging: Log code to a database or cloud storage.

Performance Improvements: Optimize CPU and memory usage.

Author
Priyansh Rajiv Dhotar

Acknowledgments
Thanks to pynput and psutil libraries.

Inspired by the need to track hand written coding progress.

