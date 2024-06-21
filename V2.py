import tkinter as tk
from tkinter import messagebox
import json
import os

class BusinessSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Hinobi: Business Simulation")
        self.company_name = ""
        self.cash = 10000
        self.reputation = 50
        self.day = 1
        self.products = 0
        self.save_slots = ["savegame1.json", "savegame2.json", "savegame3.json"]

        self.create_main_menu()

    def create_main_menu(self):
        self.clear_screen()
        tk.Label(self.root, text="Welcome to Business Simulation Game!").pack(pady=10)
        tk.Button(self.root, text="Start New Game", command=self.new_game).pack(pady=5)
        tk.Button(self.root, text="Load Game", command=self.show_load_menu).pack(pady=5)
        tk.Button(self.root, text="Delete Save", command=self.show_delete_menu).pack(pady=5)
        tk.Button(self.root, text="Quit", command=self.root.quit).pack(pady=5)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def new_game(self):
        self.clear_screen()
        tk.Label(self.root, text="Enter your company name:").pack(pady=10)
        self.company_name_entry = tk.Entry(self.root)
        self.company_name_entry.pack(pady=5)
        tk.Button(self.root, text="Start Game", command=self.start_new_game).pack(pady=10)

    def start_new_game(self):
        self.company_name = self.company_name_entry.get()
        self.cash = 10000
        self.reputation = 50
        self.day = 1
        self.products = 0
        self.clear_screen()
        tk.Label(self.root, text=f"Welcome to {self.company_name}!").pack(pady=10)
        self.game_loop()

    def save_game(self, slot):
        save_data = {
            "company_name": self.company_name,
            "cash": self.cash,
            "reputation": self.reputation,
            "day": self.day,
            "products": self.products
        }
        with open(self.save_slots[slot], "w") as file:
            json.dump(save_data, file)
        messagebox.showinfo("Save Game", f"Game saved successfully to slot {slot + 1}.")

    def load_game(self, slot):
        try:
            with open(self.save_slots[slot], "r") as file:
                save_data = json.load(file)
                self.company_name = save_data["company_name"]
                self.cash = save_data["cash"]
                self.reputation = save_data["reputation"]
                self.day = save_data["day"]
                self.products = save_data["products"]
                self.clear_screen()
                tk.Label(self.root, text=f"Welcome back to {self.company_name}!").pack(pady=10)
                self.game_loop()
        except FileNotFoundError:
            messagebox.showerror("Load Game", "No saved game found in this slot. Please choose another slot.")

    def delete_save(self, slot):
        if os.path.exists(self.save_slots[slot]):
            os.remove(self.save_slots[slot])
            messagebox.showinfo("Delete Save", f"Saved game in slot {slot + 1} deleted successfully.")
        else:
            messagebox.showerror("Delete Save", "No saved game found in this slot to delete.")

    def show_load_menu(self):
        self.clear_screen()
        tk.Label(self.root, text="Select a slot to load:").pack(pady=10)
        for i in range(3):
            tk.Button(self.root, text=f"Load Slot {i + 1}", command=lambda i=i: self.load_game(i)).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=10)

    def show_delete_menu(self):
        self.clear_screen()
        tk.Label(self.root, text="Select a slot to delete:").pack(pady=10)
        for i in range(3):
            tk.Button(self.root, text=f"Delete Slot {i + 1}", command=lambda i=i: self.delete_save(i)).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.create_main_menu).pack(pady=10)

    def game_loop(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Day {self.day}").pack(pady=10)
        tk.Label(self.root, text=f"Company: {self.company_name}").pack()
        tk.Label(self.root, text=f"Cash: ${self.cash}").pack()
        tk.Label(self.root, text=f"Reputation: {self.reputation}").pack()
        tk.Label(self.root, text=f"Products: {self.products}").pack()
        tk.Button(self.root, text="Produce products", command=self.produce_products).pack(pady=5)
        tk.Button(self.root, text="Sell products", command=self.sell_products).pack(pady=5)
        tk.Button(self.root, text="Save game", command=self.show_save_menu).pack(pady=5)
        tk.Button(self.root, text="Quit", command=self.check_bankruptcy).pack(pady=5)

    def show_save_menu(self):
        self.clear_screen()
        tk.Label(self.root, text="Select a slot to save:").pack(pady=10)
        for i in range(3):
            tk.Button(self.root, text=f"Save Slot {i + 1}", command=lambda i=i: self.save_game(i)).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.game_loop).pack(pady=10)

    def produce_products(self):
        cost = 500
        if self.cash >= cost:
            self.products += 10
            self.cash -= cost
            messagebox.showinfo("Produce Products", f"Produced 10 products for ${cost}.")
        else:
            messagebox.showerror("Produce Products", "Not enough cash to produce products.")
        self.day += 1
        self.game_loop()

    def sell_products(self):
        if self.products > 0:
            self.products -= 1
            self.cash += 1000
            self.reputation += 1
            messagebox.showinfo("Sell Products", "Sold 1 product for $1000.")
        else:
            messagebox.showerror("Sell Products", "No products to sell.")
        self.day += 1
        self.game_loop()

    def check_bankruptcy(self):
        if self.cash < 0 and self.reputation < 20:
            messagebox.showinfo("Bankruptcy", f"Your company {self.company_name} has gone bankrupt due to low cash and reputation!")
            self.create_main_menu()
        elif self.cash < 0:
            messagebox.showinfo("Bankruptcy", f"Your company {self.company_name} has gone bankrupt due to low cash!")
            self.create_main_menu()
        elif self.reputation < 20:
            messagebox.showinfo("Bankruptcy", f"Your company {self.company_name} has gone bankrupt due to low reputation!")
            self.create_main_menu()
        else:
            self.game_loop()

if __name__ == "__main__":
    root = tk.Tk()
    game = BusinessSimulation(root)
    root.mainloop()
