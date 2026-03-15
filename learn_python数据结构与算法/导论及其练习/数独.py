import tkinter as tk
from tkinter import messagebox
import random


class SudokuGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("数独游戏")
        self.root.geometry("500x600")

        # 游戏状态
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solution = None
        self.entries = []
        self.start_time = None

        # 创建界面
        self.create_widgets()

        # 生成初始谜题
        self.new_puzzle("medium")

        self.root.mainloop()

    def create_widgets(self):
        # 标题
        title_label = tk.Label(self.root, text="数独游戏",
                               font=("Arial", 20, "bold"))
        title_label.pack(pady=10)

        # 数独网格框架
        grid_frame = tk.Frame(self.root)
        grid_frame.pack()

        # 创建9x9输入框网格
        self.entries = []
        for row in range(9):
            row_entries = []
            for col in range(9):
                # 设置边框粗细来区分3x3宫格
                border_width = 2 if row % 3 == 0 and row != 0 else 1
                border_width = 2 if col % 3 == 0 and col != 0 else border_width

                entry = tk.Entry(grid_frame, width=3, font=("Arial", 18),
                                 justify='center', borderwidth=border_width,
                                 relief="solid")
                entry.grid(row=row, column=col, padx=1, pady=1)

                # 绑定验证函数，只允许输入1-9
                entry.config(validate="key",
                             validatecommand=(self.root.register(self.validate_input), '%P'))

                row_entries.append(entry)
            self.entries.append(row_entries)

        # 按钮框架
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        # 难度选择
        difficulty_label = tk.Label(button_frame, text="难度:")
        difficulty_label.grid(row=0, column=0, padx=5)

        self.difficulty_var = tk.StringVar(value="medium")
        difficulties = [("简单", "easy"), ("中等", "medium"), ("困难", "hard")]

        for i, (text, value) in enumerate(difficulties):
            rb = tk.Radiobutton(button_frame, text=text, variable=self.difficulty_var,
                                value=value)
            rb.grid(row=0, column=i + 1, padx=5)

        # 功能按钮
        new_btn = tk.Button(button_frame, text="新游戏", command=self.new_game,
                            width=10)
        new_btn.grid(row=1, column=0, padx=5, pady=10)

        solve_btn = tk.Button(button_frame, text="求解", command=self.solve,
                              width=10)
        solve_btn.grid(row=1, column=1, padx=5, pady=10)

        check_btn = tk.Button(button_frame, text="检查", command=self.check,
                              width=10)
        check_btn.grid(row=1, column=2, padx=5, pady=10)

        hint_btn = tk.Button(button_frame, text="提示", command=self.give_hint,
                             width=10)
        hint_btn.grid(row=1, column=3, padx=5, pady=10)

        # 状态标签
        self.status_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.status_label.pack(pady=10)

    def validate_input(self, text):
        """验证输入，只允许1-9或空字符串"""
        if text == "" or (text.isdigit() and 1 <= int(text) <= 9):
            return True
        return False

    def new_puzzle(self, difficulty):
        """生成新的数独谜题"""
        # 生成完整解
        self.solution = self.generate_full_sudoku()

        # 生成谜题
        self.board = self.generate_puzzle(self.solution, difficulty)

        # 更新界面
        self.update_display()

        # 重置状态
        self.start_time = None
        self.status_label.config(text="新游戏开始！")

    def new_game(self):
        """开始新游戏"""
        self.new_puzzle(self.difficulty_var.get())

    def update_display(self):
        """更新界面显示"""
        for row in range(9):
            for col in range(9):
                entry = self.entries[row][col]
                entry.delete(0, tk.END)

                if self.board[row][col] != 0:
                    entry.insert(0, str(self.board[row][col]))
                    entry.config(state='readonly', readonlybackground='#f0f0f0')
                else:
                    entry.config(state='normal', bg='white')

    def solve(self):
        """求解当前数独"""
        # 复制当前板
        temp_board = [row[:] for row in self.board]

        if self.solve_sudoku(temp_board):
            # 显示解
            for row in range(9):
                for col in range(9):
                    if self.board[row][col] == 0:
                        self.entries[row][col].delete(0, tk.END)
                        self.entries[row][col].insert(0, str(temp_board[row][col]))
                        self.entries[row][col].config(bg='#e0ffe0')  # 绿色背景标记
            self.status_label.config(text="已求解！")
        else:
            messagebox.showerror("错误", "此数独无解！")

    def check(self):
        """检查当前填写是否正确"""
        # 获取用户输入
        user_board = [[0 for _ in range(9)] for _ in range(9)]

        for row in range(9):
            for col in range(9):
                entry_text = self.entries[row][col].get()
                if entry_text:
                    user_board[row][col] = int(entry_text)
                else:
                    user_board[row][col] = 0

        # 检查是否完成
        complete = True
        for row in range(9):
            for col in range(9):
                if user_board[row][col] == 0:
                    complete = False
                    break

        if not complete:
            messagebox.showinfo("检查", "还有空白格子未填写！")
            return

        # 验证是否正确
        if self.is_valid_solution(user_board):
            messagebox.showinfo("恭喜", "解答正确！")
            self.status_label.config(text="解答正确！")
        else:
            messagebox.showerror("错误", "解答有误，请检查！")

    def give_hint(self):
        """提供一个提示"""
        # 找到第一个空白格
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0 and not self.entries[row][col].get():
                    # 显示正确答案
                    self.entries[row][col].delete(0, tk.END)
                    self.entries[row][col].insert(0, str(self.solution[row][col]))
                    self.entries[row][col].config(bg='#fff0e0')  # 橙色背景提示
                    self.status_label.config(text=f"提示：第{row + 1}行第{col + 1}列")
                    return

        messagebox.showinfo("提示", "所有格子都已填写！")

    def is_valid_solution(self, board):
        """验证数独解是否正确"""
        # 检查行
        for row in board:
            if sorted(row) != list(range(1, 10)):
                return False

        # 检查列
        for col in range(9):
            column = [board[row][col] for row in range(9)]
            if sorted(column) != list(range(1, 10)):
                return False

        # 检查3x3宫格
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box = []
                for i in range(3):
                    for j in range(3):
                        box.append(board[box_row + i][box_col + j])
                if sorted(box) != list(range(1, 10)):
                    return False

        return True

    def generate_full_sudoku(self):
        """生成完整的数独解"""
        board = [[0 for _ in range(9)] for _ in range(9)]

        # 填充对角线宫格
        for box in range(0, 9, 3):
            numbers = list(range(1, 10))
            random.shuffle(numbers)
            for i in range(3):
                for j in range(3):
                    board[box + i][box + j] = numbers.pop()

        # 使用回溯法填充
        def fill_board(board):
            for row in range(9):
                for col in range(9):
                    if board[row][col] == 0:
                        numbers = list(range(1, 10))
                        random.shuffle(numbers)
                        for num in numbers:
                            if self.is_valid_position(board, row, col, num):
                                board[row][col] = num
                                if fill_board(board):
                                    return True
                                board[row][col] = 0
                        return False
            return True

        fill_board(board)
        return board

    def generate_puzzle(self, solution, difficulty):
        """从完整解生成谜题，根据难度移除数字"""
        board = [row[:] for row in solution]

        if difficulty == "easy":
            cells_to_remove = random.randint(30, 40)
        elif difficulty == "medium":
            cells_to_remove = random.randint(40, 50)
        elif difficulty == "hard":
            cells_to_remove = random.randint(50, 60)
        else:
            cells_to_remove = 40

        positions = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(positions)

        for i, j in positions[:cells_to_remove]:
            board[i][j] = 0

        return board

    def is_valid_position(self, board, row, col, num):
        """检查位置是否有效"""
        # 检查行
        for i in range(9):
            if board[row][i] == num:
                return False

        # 检查列
        for i in range(9):
            if board[i][col] == num:
                return False

        # 检查3x3宫格
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num:
                    return False

        return True

    def solve_sudoku(self, board):
        """求解数独"""
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid_position(board, row, col, num):
                            board[row][col] = num
                            if self.solve_sudoku(board):
                                return True
                            board[row][col] = 0
                    return False
        return True


# 启动游戏
if __name__ == "__main__":
    game = SudokuGame()

