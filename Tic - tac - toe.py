import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Крестики-нолики - Полный экран")
        
        # На весь экран
        self.window.attributes('-fullscreen', True)
        
        # Привязка клавиши Escape для выхода из полноэкранного режима
        self.window.bind('<Escape>', self.toggle_fullscreen)
        
        # Цвета
        self.bg_color = '#2c3e50'
        self.button_bg = '#ecf0f1'
        self.button_active = '#bdc3c7'
        
        # Переменные игры
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.game_over = False
        self.player_turn = True
        self.fullscreen = True
        
        # Настройка главного окна
        self.window.configure(bg=self.bg_color)
        
        # Создание адаптивного интерфейса
        self.create_widgets()
        
        # Адаптация при изменении размера окна
        self.window.bind('<Configure>', self.on_resize)
        
        # Если компьютер ходит первым
        if not self.player_turn:
            self.window.after(500, self.computer_move)
        
        self.window.mainloop()
    
    def toggle_fullscreen(self, event=None):
        """Переключение полноэкранного режима"""
        self.fullscreen = not self.fullscreen
        self.window.attributes('-fullscreen', self.fullscreen)
    
    def on_resize(self, event):
        """Адаптация размеров при изменении окна"""
        # Получаем размеры окна
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        
        # Адаптируем размер шрифтов под размер окна
        if width > 800:
            title_size = min(36, width // 15)
            status_size = min(24, width // 20)
            button_size = min(60, width // 12)
        else:
            title_size = 24
            status_size = 16
            button_size = 40
        
        # Обновляем шрифты
        self.title_label.config(font=('Arial', title_size, 'bold'))
        self.status_label.config(font=('Arial', status_size, 'bold'))
        self.reset_button.config(font=('Arial', max(12, status_size // 2), 'bold'))
        
        # Обновляем шрифты кнопок игрового поля
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j]:
                    self.buttons[i][j].config(font=('Arial', button_size, 'bold'))
        
        # Адаптируем отступы
        self.update_idletasks()
    
    def create_widgets(self):
        """Создание всех элементов интерфейса"""
        # Основной контейнер с отступами
        self.main_frame = tk.Frame(self.window, bg=self.bg_color)
        self.main_frame.pack(expand=True, fill='both', padx=50, pady=50)
        
        # Верхняя часть с заголовком и статусом
        top_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        top_frame.pack(side='top', fill='x', pady=(0, 30))
        
        # Заголовок
        self.title_label = tk.Label(
            top_frame, 
            text="✨ КРЕСТИКИ-НОЛИКИ ✨", 
            font=('Arial', 36, 'bold'),
            fg='#ecf0f1',
            bg=self.bg_color
        )
        self.title_label.pack(pady=(0, 20))
        
        # Статус игры
        self.status_label = tk.Label(
            top_frame,
            text="🎮 Ваш ход (X)",
            font=('Arial', 24, 'bold'),
            fg='#2ecc71',
            bg=self.bg_color
        )
        self.status_label.pack()
        
        # Игровое поле (центр)
        self.board_frame = tk.Frame(self.main_frame, bg='#34495e', relief='ridge', bd=5)
        self.board_frame.pack(expand=True, pady=30)
        
        # Создание кнопок 3x3
        for i in range(3):
            self.board_frame.grid_rowconfigure(i, weight=1)
            self.board_frame.grid_columnconfigure(i, weight=1)
            for j in range(3):
                self.buttons[i][j] = tk.Button(
                    self.board_frame,
                    text='',
                    font=('Arial', 60, 'bold'),
                    command=lambda row=i, col=j: self.player_click(row, col),
                    bg=self.button_bg,
                    activebackground=self.button_active,
                    relief='raised',
                    bd=5,
                    cursor='hand2'
                )
                self.buttons[i][j].grid(row=i, column=j, padx=10, pady=10, sticky='nsew')
        
        # Нижняя часть с кнопками
        bottom_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        bottom_frame.pack(side='bottom', fill='x', pady=(30, 0))
        
        # Кнопка новой игры
        self.reset_button = tk.Button(
            bottom_frame,
            text="🔄 НОВАЯ ИГРА",
            font=('Arial', 16, 'bold'),
            command=self.reset_game,
            bg='#e74c3c',
            fg='white',
            activebackground='#c0392b',
            activeforeground='white',
            cursor='hand2',
            width=20,
            height=2,
            relief='raised',
            bd=3
        )
        self.reset_button.pack(pady=(0, 20))
        
        # Подсказка
        hint_label = tk.Label(
            bottom_frame,
            text="💡 Нажмите ESC для выхода из полноэкранного режима | Просто нажмите на клетку, чтобы сделать ход",
            font=('Arial', 12),
            fg='#95a5a6',
            bg=self.bg_color
        )
        hint_label.pack()
    
    def player_click(self, row, col):
        """Обработка клика игрока"""
        if not self.game_over and self.player_turn and self.board[row][col] == ' ':
            # Ход игрока
            self.make_move(row, col, 'X')
            
            # Проверка на победу/ничью
            if not self.game_over:
                self.player_turn = False
                self.status_label.config(text="🤖 Ход компьютера (O)", fg='#e74c3c')
                self.window.update()
                # Ход компьютера с небольшой задержкой
                self.window.after(500, self.computer_move)
    
    def make_move(self, row, col, player):
        """Совершить ход"""
        self.board[row][col] = player
        
        # Настройка цвета в зависимости от игрока
        if player == 'X':
            color = '#3498db'  # синий для X
            text = '❌'
        else:
            color = '#e74c3c'  # красный для O
            text = '⭕'
        
        self.buttons[row][col].config(text=text, fg=color)
        
        # Проверка на победу
        if self.check_winner(player):
            self.game_over = True
            if player == 'X':
                self.status_label.config(text="🎉 ПОБЕДА! Вы великолепны! 🎉", fg='#2ecc71')
                messagebox.showinfo("Победа!", "🎉 Поздравляю! Вы победили компьютер! 🎉")
            else:
                self.status_label.config(text="💀 ПОРАЖЕНИЕ! Компьютер победил 💀", fg='#e74c3c')
                messagebox.showinfo("Поражение", "😢 Компьютер выиграл. Попробуйте ещё раз!")
            return
        
        # Проверка на ничью
        if self.is_board_full():
            self.game_over = True
            self.status_label.config(text="🤝 НИЧЬЯ! Отличная игра! 🤝", fg='#f39c12')
            messagebox.showinfo("Ничья!", "🤝 Ничья! Хорошая игра!")
            return
    
    def computer_move(self):
        """Ход компьютера"""
        if not self.game_over and not self.player_turn:
            # Находим лучший ход
            row, col = self.get_best_move()
            
            if row is not None and col is not None:
                self.make_move(row, col, 'O')
                
                # Проверка на окончание игры
                if not self.game_over:
                    self.player_turn = True
                    self.status_label.config(text="🎮 Ваш ход (X)", fg='#2ecc71')
    
    def get_best_move(self):
        """AI: выбор лучшего хода"""
        empty_cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ' ']
        
        # 1. Выигрыш компьютера
        for row, col in empty_cells:
            self.board[row][col] = 'O'
            if self.check_winner('O'):
                self.board[row][col] = ' '
                return row, col
            self.board[row][col] = ' '
        
        # 2. Блокировка победы игрока
        for row, col in empty_cells:
            self.board[row][col] = 'X'
            if self.check_winner('X'):
                self.board[row][col] = ' '
                return row, col
            self.board[row][col] = ' '
        
        # 3. Занимаем центр
        if self.board[1][1] == ' ':
            return 1, 1
        
        # 4. Занимаем углы
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        available_corners = [corner for corner in corners if self.board[corner[0]][corner[1]] == ' ']
        if available_corners:
            return random.choice(available_corners)
        
        # 5. Любой свободный ход
        if empty_cells:
            return random.choice(empty_cells)
        
        return None, None
    
    def check_winner(self, player):
        """Проверка победы"""
        # Строки и столбцы
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)):
                self.highlight_winner_cells([(i, j) for j in range(3)])
                return True
            if all(self.board[j][i] == player for j in range(3)):
                self.highlight_winner_cells([(j, i) for j in range(3)])
                return True
        
        # Диагонали
        if all(self.board[i][i] == player for i in range(3)):
            self.highlight_winner_cells([(i, i) for i in range(3)])
            return True
        if all(self.board[i][2-i] == player for i in range(3)):
            self.highlight_winner_cells([(i, 2-i) for i in range(3)])
            return True
        
        return False
    
    def highlight_winner_cells(self, cells):
        """Подсветка выигрышной линии"""
        for row, col in cells:
            self.buttons[row][col].config(bg='#f1c40f', relief='sunken')
    
    def is_board_full(self):
        """Проверка на заполненность поля"""
        return all(self.board[i][j] != ' ' for i in range(3) for j in range(3))
    
    def reset_game(self):
        """Сброс игры"""
        # Очистка поля
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.game_over = False
        
        # Очистка кнопок
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text='', bg=self.button_bg, relief='raised')
        
        # Случайный выбор первого хода
        self.player_turn = random.choice([True, False])
        
        if self.player_turn:
            self.status_label.config(text="🎮 Ваш ход (X)", fg='#2ecc71')
        else:
            self.status_label.config(text="🤖 Ход компьютера (O)", fg='#e74c3c')
            self.window.after(500, self.computer_move)

# Запуск игры
if __name__ == "__main__":
    game = TicTacToe()