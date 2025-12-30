import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import axelrod as axl
from util import createPlayer
from pathlib import Path


class StrategyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Strategy selector")
        self.root.geometry("600x300")
        self.root.resizable(False, False)
        self.root.grid_columnconfigure(0, weight=2)
        self.root.grid_columnconfigure(1, weight=2)
        self.root.grid_rowconfigure(0, weight=1)

        main_frame = ttk.Frame(self.root, padding="10")
        strategies_frame = ttk.Frame(self.root, padding="10")
        confirm_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="news")
        strategies_frame.grid(row=0, column=1, sticky="news")
        confirm_frame.grid(row=1, column=0, sticky="news")

        title_label = ttk.Label(
            main_frame, text="Select strategies", font=("Helvetica", 25)
        )
        strategies_label = ttk.Label(
            strategies_frame, text="Selected strategies", font=("Helvetica", 16)
        )
        title_label.pack()
        strategies_label.pack()
        strategy_label = ttk.Label(main_frame, text="Strategy:")
        strategy_label.pack()
        ##
        self.selected_strategies = []
        self.strategy_var = tk.StringVar()
        self.strategy_dropdown = ttk.Combobox(
            main_frame,
            textvariable=self.strategy_var,
            state="readonly",
            width=25)

        folder = Path("../custom-strategies/")
        custom_strategies = [p.name for p in folder.glob("*.py")]
        standard_strategies = ("Tit for Tat", "Pavlov", "Always Cooperate", "Always Defect", "Random")
        self.strategy_dropdown["values"] = standard_strategies + tuple(custom_strategies)
        self.strategy_dropdown.current(0)
        self.strategy_dropdown.pack()
        # self.strategy_dropdown.bind("<<ComboboxSelected>>", self.on_strategy_change)
        self.selected_frame = ttk.Frame(strategies_frame)
        self.selected_frame.pack(fill="both", expand=True)
        self.custom_label = ttk.Label(main_frame, text="Custom Strategy File:")
        self.custom_entry = ttk.Entry(main_frame, width=27, state="disabled")
        self.custom_button = ttk.Button(
            main_frame, text="Browse", command=self.browse_file, state="disabled"
        )
        
        add_button = ttk.Button(
            main_frame,
            text="Add strategy",
            command=self.add_strategy,
            padding=10)
        add_button.pack(padx=10, pady=10) 
        ##
        iterations_label = ttk.Label(confirm_frame, text="Number of Iterations:")
        iterations_label.pack()
        self.iterations_var = tk.StringVar(value="100")
        iterations_entry = ttk.Entry(
            confirm_frame, textvariable=self.iterations_var, width=27
        )
        iterations_entry.pack()

        button_frame = ttk.Frame(confirm_frame)
        button_frame.pack()
        run_button = ttk.Button(
            button_frame,
            text="Run Simulation",
            command=self.run_simulation,
            padding=10)
        run_button.grid(row=0, column=0, sticky="news", padx=5, pady=5)
        reset_button = ttk.Button(
            button_frame,
            text="Reset",
            command=self.reset_fields,
            padding=10)
        reset_button.grid(row=0, column=1, sticky="news", padx=5, pady=5)
        
        ##ovo je ružno, ali ajde 
        self.need_to_remember_this_frame = confirm_frame


    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
        if file_path:
            self.custom_entry.delete(0, tk.END)
            self.custom_entry.insert(0, file_path)


    def add_strategy(self):
        value = self.strategy_var.get()
        if value not in self.selected_strategies:
            self.selected_strategies.append(value)
            item_frame = ttk.Frame(self.selected_frame)
            item_frame.pack(fill="x", pady=2)
            lbl = ttk.Label(item_frame, text=value)
            lbl.pack(side="left", padx=(0,10))

            btn = ttk.Button(item_frame,
                             text="x",
                             width=2,
                            command=lambda f=item_frame, v=value: self.remove_strategy(f, v))
            btn.pack(side="right")


    def remove_strategy(self, frame, value):
        frame.destroy()
        if value in self.selected_strategies:
            self.selected_strategies.remove(value)


    def run_simulation(self):
        players = []
        for strategy_name in self.selected_strategies:
            if strategy_name.endswith(".py"):
                print(strategy_name)
                player = createPlayer(strategy_name[:-3], "../custom-strategies/" + strategy_name)
                players.append(player)
            else: 
                if strategy_name == "Tit for Tat":
                    players.append(axl.TitForTat())
                elif strategy_name == "Pavlov":
                    players.append(axl.WinStayLoseShift())
                elif strategy_name == "Always Cooperate":
                    players.append(axl.Cooperator())
                elif strategy_name == "Always Defect":
                    players.append(axl.Defector())
                elif strategy_name == "Random":
                    players.append(axl.Random())

        tournament = axl.Tournament(
                                    players,
                                    turns=int(self.iterations_var.get()),
                                    repetitions=3)
        self.results = tournament.play()
        print(self.results.ranked_names)
        visuals_button = ttk.Button(
            self.need_to_remember_this_frame,
            text="Visualize results",
            command=self.plot,
            padding=10)
        visuals_button.pack()
        
    def plot(self):
        # Create the main plotting object
        plot = axl.Plot(self.results)

        box = plot.boxplot()
        box.show()

        win = plot.winplot()
        win.show()

        payoff = plot.payoff()
        payoff.show()

        return plot

    def reset_fields(self):
        self.strategy_dropdown.current(0)
        self.iterations_var.set("100")
        self.custom_entry.delete(0, tk.END)
        self.selected_strategies.clear()
        for child in self.selected_frame.winfo_children():
            child.destroy()


def main():
    root = tk.Tk()
    app = StrategyGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
