import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta


class GameTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Session Timer")
        self.root.geometry("500x350")
        self.root.configure(bg="#f0f0f0")

        # Configure styles
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Helvetica", 12, "bold"), padding=6)
        self.style.configure("TLabel", font=("Helvetica", 24, "bold"), foreground="#333333")
        self.style.map("TButton",
                       foreground=[("active", "#ffffff"), ("pressed", "#ffffff")],
                       background=[("active", "#007acc"), ("pressed", "#005fa3")])

        self.start_time = None
        self.elapsed_time = timedelta(0)
        self.is_running = False

        # Timer Label
        self.timer_label = ttk.Label(root, text="00:00:00")
        self.timer_label.pack(pady=20)

        # Total Playtime Label
        self.total_label = ttk.Label(root, text="Total Today: 00:00:00")
        self.total_label.pack(pady=10)

        # Control Buttons
        self.button_frame = ttk.Frame(root)
        self.button_frame.pack(pady=10)

        self.start_button = ttk.Button(self.button_frame, text="Start", command=self.start_timer, width=10)
        self.start_button.grid(row=0, column=0, padx=5)

        self.pause_button = ttk.Button(self.button_frame, text="Pause", command=self.pause_timer, width=10)
        self.pause_button.grid(row=0, column=1, padx=5)

        self.reset_button = ttk.Button(self.button_frame, text="Reset", command=self.reset_timer, width=10)
        self.reset_button.grid(row=0, column=2, padx=5)

        self.history_button = ttk.Button(root, text="View History", command=self.view_history, width=30)
        self.history_button.pack(pady=10)

        self.update_timer()

    def start_timer(self):
        if not self.is_running:
            self.start_time = datetime.now() - self.elapsed_time
            self.is_running = True
            self.start_button.state(["disabled"])
            self.pause_button.state(["!disabled"])

    def pause_timer(self):
        if self.is_running:
            self.elapsed_time = datetime.now() - self.start_time
            self.is_running = False
            self.start_button.state(["!disabled"])
            self.pause_button.state(["disabled"])

    def reset_timer(self):
        self.elapsed_time = timedelta(0)
        self.timer_label.config(text="00:00:00")
        self.start_button.state(["!disabled"])
        self.pause_button.state(["disabled"])
        self.is_running = False

    def update_timer(self):
        if self.is_running:
            current_time = datetime.now() - self.start_time
            self.timer_label.config(text=str(current_time).split(".")[0])
        self.update_total_playtime()
        self.root.after(1000, self.update_timer)

    def update_total_playtime(self):
        today = datetime.now().date()
        total_playtime = timedelta()
        try:
            with open("session_logs.txt", "r") as f:
                for line in f:
                    parts = line.split(", ")
                    start_str = parts[0].split(": ")[1].strip()
                    end_str = parts[1].split(": ")[1].strip()
                    start_time = datetime.strptime(start_str.split('.')[0], '%Y-%m-%d %H:%M:%S')
                    end_time = datetime.strptime(end_str.split('.')[0], '%Y-%m-%d %H:%M:%S')
                    if start_time.date() == today:
                        duration = end_time - start_time
                        total_playtime += duration
        except FileNotFoundError:
            pass
        self.total_label.config(text=f"Total Today: {str(total_playtime).split('.')[0]}")

    def log_session(self, start, end, duration):
        with open("session_logs.txt", "a") as f:
            log_entry = f"Start: {start}, End: {end}, Duration: {duration}\n"
            f.write(log_entry)

    def view_history(self):
        try:
            with open("session_logs.txt", "r") as f:
                history = f.read()
            messagebox.showinfo("Session History", history if history else "No sessions logged yet.")
        except FileNotFoundError:
            messagebox.showinfo("Session History", "No sessions logged yet.")


if __name__ == "__main__":
    root = tk.Tk()
    app = GameTimerApp(root)
    root.mainloop()
