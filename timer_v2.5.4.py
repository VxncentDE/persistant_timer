import tkinter as tk
import time
import pickle
import os

# File to store the start timestamp and other data
TIME_FILE = "start_time.pkl"

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Persistent Timer")
        self.root.geometry("400x300")  # Set the window size to be bigger

        self.start_time = None  # To store the initial start time
        self.elapsed_time = 0   # To store the elapsed time
        self.running = False
        self.paused = False  # Flag for paused state
        self.pause_start_time = 0  # Timestamp of when pause started
        self.pause_duration = 0  # Total pause duration

        # Load saved start time if it exists
        self.load_start_time()

        # Create UI components
        self.time_label = tk.Label(root, text="00:00:00", font=("Helvetica", 36))
        self.time_label.pack(pady=20)

        self.start_button = tk.Button(root, text="Start", command=self.start_timer, width=15)
        self.start_button.pack(pady=5)

        self.pause_button = tk.Button(root, text="Pause", command=self.pause_timer, width=15)
        self.pause_button.pack(pady=5)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset_timer, width=15)
        self.reset_button.pack(pady=5)

        self.exit_button = tk.Button(root, text="Exit", command=self.root.quit, width=15)
        self.exit_button.pack(pady=5)

        # Update the timer display
        self.update_timer()

    def start_timer(self):
        if not self.running:
            if self.start_time is None:
                # If the timer has not been started yet, set the current time as the start
                self.start_time = time.time()
                self.pause_duration = 0  # Reset pause duration
                self.save_start_time()
            elif self.paused:
                # If it was paused, calculate pause duration and resume
                self.pause_duration += time.time() - self.pause_start_time  # Accumulate paused time
                self.paused = False
            self.running = True
            self.save_start_time()

    def pause_timer(self):
        if self.running:
            self.running = False
            self.paused = True
            self.pause_start_time = time.time()  # Record the time when pause started
            self.save_start_time()

    def reset_timer(self):
        # Clear start time and reset everything
        self.start_time = None
        self.elapsed_time = 0
        self.running = False
        self.paused = False
        self.pause_duration = 0
        self.save_start_time()  # Clear saved time
        self.update_timer_display()

    def update_timer(self):
        if self.running and self.start_time is not None:
            # Calculate elapsed time since start time, minus the total pause duration
            self.elapsed_time = time.time() - self.start_time - self.pause_duration

        # Update the display
        self.update_timer_display()

        # Call this function again after 1 second (1000 milliseconds)
        self.root.after(1000, self.update_timer)

    def update_timer_display(self):
        # Format elapsed time as hours:minutes:seconds
        hours, remainder = divmod(int(self.elapsed_time), 3600)
        minutes, seconds = divmod(remainder, 60)
        self.time_label.config(text=f"{hours:02}:{minutes:02}:{seconds:02}")

    def save_start_time(self):
        # Save the start time, pause status, and pause duration to a file using pickle
        data = {
            'start_time': self.start_time,
            'pause_duration': self.pause_duration,
            'paused': self.paused,
            'pause_start_time': self.pause_start_time  # When the pause started
        }
        with open(TIME_FILE, 'wb') as f:
            pickle.dump(data, f)

    def load_start_time(self):
        # Load the start time, pause status, and pause duration from file if it exists
        if os.path.exists(TIME_FILE):
            with open(TIME_FILE, 'rb') as f:
                data = pickle.load(f)

            # Load start time, pause duration, and paused status
            self.start_time = data.get('start_time')
            self.pause_duration = data.get('pause_duration', 0)
            self.paused = data.get('paused', False)
            self.pause_start_time = data.get('pause_start_time', 0)

            if self.start_time is not None:
                if self.paused:
                    # If paused, calculate elapsed time up to when it was paused
                    self.elapsed_time = self.pause_start_time - self.start_time - self.pause_duration
                    self.running = False
                else:
                    # If the timer was running, calculate elapsed time properly
                    self.elapsed_time = time.time() - self.start_time - self.pause_duration
                    self.running = True
            else:
                # If the start_time is None (meaning it hasn't started), set elapsed time to 0
                self.elapsed_time = 0

# Create the main application window
root = tk.Tk()
app = TimerApp(root)

# Start the Tkinter main loop
root.mainloop()
