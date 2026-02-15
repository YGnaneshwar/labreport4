import tkinter as tk 
from tkinter import messagebox 
import random, time 
 
N = 9  # Sudoku grid size 
DELAY = 100  # delay in ms to visualize steps 
 
class SudokuGUI: 
    def __init__(self, root):   # fixed constructor 
        self.root = root 
        self.root.title("Sudoku Solver - Version 2")
        self.entries = [[None for _ in range(N)] for _ in range(N)] 
 
        # Create Sudoku Grid 
        frame = tk.Frame(root) 
        frame.pack(pady=20) 
 
        for i in range(N): 
            for j in range(N): 
  
  

 
                entry = tk.Entry(frame, width=3, font=('Arial', 18), justify='center', 
                                 borderwidth=1, relief="solid") 
                entry.grid(row=i, column=j, padx=2, pady=2) 
                self.entries[i][j] = entry 
 
        # Difficulty selection 
        difficulty_frame = tk.Frame(root) 
        difficulty_frame.pack(pady=10) 
        tk.Label(difficulty_frame, text="Difficulty:").grid(row=0, column=0, padx=5) 
 
        self.difficulty_var = tk.StringVar(value="Beginner") 
        self.difficulty_menu = tk.OptionMenu(difficulty_frame, self.difficulty_var, "Beginner", 
"Normal", "Expert") 
        self.difficulty_menu.grid(row=0, column=1, padx=5) 
 
        # Buttons 
        button_frame = tk.Frame(root) 
        button_frame.pack(pady=10) 
 
        tk.Button(button_frame, text="Generate Puzzle", command=self.generate_puzzle).grid(row=0, 
column=0, padx=10) 
        tk.Button(button_frame, text="Solve", command=self.solve).grid(row=0, column=1, padx=10) 
        tk.Button(button_frame, text="Clear", command=self.clear).grid(row=0, column=2, padx=10) 
 
    def get_board(self): 
        """Fetch numbers from GUI grid""" 
        board = [] 
        for i in range(N): 
            row = [] 
            for j in range(N): 
                val = self.entries[i][j].get() 
  
  
 
                row.append(int(val) if val.isdigit() else 0) 
            board.append(row) 
        return board 
 
    def set_board(self, board): 
        """Set board values in GUI""" 
        self.clear() 
        for i in range(N): 
            for j in range(N): 
                if board[i][j] != 0: 
                    self.entries[i][j].insert(0, str(board[i][j])) 
 
    def color_cell(self, row, col, color, value=""): 
        """Color a cell and optionally set value""" 
        self.entries[row][col].delete(0, tk.END) 
        if value != 0 and value != "": 
            self.entries[row][col].insert(0, str(value)) 
        self.entries[row][col].config(bg=color) 
        self.root.update() 
        self.root.after(DELAY) 
 
    def solve(self): 
        board = self.get_board() 
        start_time = time.time()  # Start timer 
 
        if self.solve_backtrack(board): 
            end_time = time.time() 
            elapsed = round(end_time - start_time, 2) 
            messagebox.showinfo("Success", f"Sudoku Solved!\nTime Taken: {elapsed} seconds") 
        else: 
            messagebox.showerror("Error", "No solution exists!") 
  
  
 
 
    def solve_backtrack(self, board): 
        empty = self.find_empty(board) 
        if not empty: 
            return True  # Solved 
 
        row, col = empty 
        for num in range(1, 10): 
            if self.is_safe(board, row, col, num): 
                # Try number (visualize in green) 
                board[row][col] = num 
                self.color_cell(row, col, "lightgreen", num) 
 
                if self.solve_backtrack(board): 
                    return True 
 
                # Backtrack (visualize in red) 
                board[row][col] = 0 
                self.color_cell(row, col, "lightcoral", "") 
 
        return False 
 
    def is_safe(self, board, row, col, num): 
        if num in board[row]: 
            return False 
        for i in range(N): 
            if board[i][col] == num: 
                return False 
        start_row, start_col = 3 * (row // 3), 3 * (col // 3) 
        for i in range(start_row, start_row + 3): 
            for j in range(start_col, start_col + 3): 
  
  
 
                if board[i][j] == num: 
                    return False 
        return True 
 
    def find_empty(self, board): 
        for i in range(N): 
            for j in range(N): 
                if board[i][j] == 0: 
                    return i, j 
        return None 
 
    def clear(self): 
        for i in range(N): 
            for j in range(N): 
                self.entries[i][j].delete(0, tk.END) 
                self.entries[i][j].config(bg="white") 
 
    def generate_puzzle(self): 
        """Generate a Sudoku puzzle based on difficulty""" 
        # Base solved board (static for simplicity) 
        solved = [ 
            [5, 3, 4, 6, 7, 8, 9, 1, 2], 
            [6, 7, 2, 1, 9, 5, 3, 4, 8], 
            [1, 9, 8, 3, 4, 2, 5, 6, 7], 
            [8, 5, 9, 7, 6, 1, 4, 2, 3], 
            [4, 2, 6, 8, 5, 3, 7, 9, 1], 
            [7, 1, 3, 9, 2, 4, 8, 5, 6], 
            [9, 6, 1, 5, 3, 7, 2, 8, 4], 
            [2, 8, 7, 4, 1, 9, 6, 3, 5], 
            [3, 4, 5, 2, 8, 6, 1, 7, 9] 
        ] 
  
  
 
 
        puzzle = [row[:] for row in solved] 
 
        # Difficulty levels 
        difficulty = self.difficulty_var.get() 
        if difficulty == "Beginner": 
            cells_to_remove = 30 
        elif difficulty == "Normal": 
            cells_to_remove = 45 
        else:  # Expert 
            cells_to_remove = 60 
 
        # Randomly remove cells 
        for _ in range(cells_to_remove): 
            i, j = random.randint(0, 8), random.randint(0, 8) 
            puzzle[i][j] = 0 
 
        self.set_board(puzzle) 
 
# ---------------- Run App ---------------- 
if __name__ == "__main__":   # fixed entry point 
    root = tk.Tk() 
    app = SudokuGUI(root) 
    root.mainloop() 