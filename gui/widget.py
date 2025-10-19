import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import axelrod as axl
from util import createPlayer


class StrategyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Strategy selector")
        self.root.geometry("600x300")
        self.root.resizable(False, False)

        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        title_label = ttk.Label(
            main_frame, text="Select a Strategy", font=("Helvetica", 16)
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        strategy_label = ttk.Label(main_frame, text="Strategy:")
        strategy_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        self.strategy_var = tk.StringVar()
        self.strategy_dropdown = ttk.Combobox(
            main_frame, textvariable=self.strategy_var, state="readonly", width=25
        )
        self.strategy_dropdown["values"] = ("Tit for Tat", "Pavlov", "Custom Strategy")
        self.strategy_dropdown.current(0)
        self.strategy_dropdown.grid(row=1, column=1, pady=5, padx=(10, 0))
        self.strategy_dropdown.bind("<<ComboboxSelected>>", self.on_strategy_change)

        self.custom_label = ttk.Label(main_frame, text="Custom Strategy File:")
        self.custom_entry = ttk.Entry(main_frame, width=27, state="disabled")
        self.custom_button = ttk.Button(
            main_frame, text="Browse", command=self.browse_file, state="disabled"
        )

        iterations_label = ttk.Label(main_frame, text="Number of Iterations:")
        iterations_label.grid(row=3, column=0, sticky=tk.W, pady=5)
        self.iterations_var = tk.StringVar(value="100")
        iterations_entry = ttk.Entry(
            main_frame, textvariable=self.iterations_var, width=27
        )
        iterations_entry.grid(row=3, column=1, pady=5, padx=(10, 0))

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=(20, 0))
        run_button = ttk.Button(
            button_frame, text="Run Simulation", command=self.run_simulation
        )
        run_button.grid(row=0, column=0, padx=5)
        reset_button = ttk.Button(button_frame, text="Reset", command=self.reset_fields)
        reset_button.grid(row=0, column=1, padx=5)

    def on_strategy_change(self, event):
        if self.strategy_var.get() == "Custom Strategy":
            self.custom_label.grid(row=2, column=0, sticky=tk.W, pady=5)
            self.custom_entry.grid(row=2, column=1, pady=5, padx=(10, 0))
            self.custom_button.grid(row=2, column=2, pady=5)
            self.custom_entry.config(state="normal")
            self.custom_button.config(state="normal")
        else:
            self.custom_label.grid_remove()
            self.custom_entry.grid_remove()
            self.custom_button.grid_remove()
            self.custom_entry.config(state="disabled")
            self.custom_button.config(state="disabled")

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
        if file_path:
            self.custom_entry.delete(0, tk.END)
            self.custom_entry.insert(0, file_path)

    def run_simulation(self):
        strategy_name = self.strategy_var.get()
        iterations = self.iterations_var.get()

        try:
            turns = int(iterations)
            if turns <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid Input", "Please enter a valid positive integer for iterations."
            )
            return

        if strategy_name == "Custom Strategy":
            file_path = self.custom_entry.get()
            if not file_path:
                messagebox.showerror(
                    "Invalid Input", "Please select a custom strategy file."
                )
                return
            try:
                strategy = createPlayer(strategy_name, file_path)
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Failed to load custom strategy: {str(e)}"
                )
                return
        else:
            strategy_map = {
                "Tit for Tat": axl.TitForTat(),
                "Pavlov": axl.WinStayLoseShift(),
            }
            strategy = strategy_map.get(strategy_name)
            if not strategy:
                messagebox.showerror("Error", "Unknown strategy.")
                return

        opponent = axl.Cooperator()
        match = axl.Match([strategy, opponent], turns=turns)
        results = match.play()
        scores = match.final_score()

        message = f"Strategy: {strategy_name}\nOpponent: {opponent}\nTurns: {turns}\nFinal Scores: {scores}"
        messagebox.showinfo("Simulation Results", message)
        print(f"Results: {results}")
        print(f"Scores: {scores}")

    def reset_fields(self):
        self.strategy_dropdown.current(0)
        self.iterations_var.set("100")
        self.custom_entry.delete(0, tk.END)
        self.on_strategy_change(None)


def main():
    root = tk.Tk()
    app = StrategyGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
