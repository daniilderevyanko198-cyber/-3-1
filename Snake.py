import tkinter as tk
import random
from tkinter import messagebox

class SnakeGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Змейка - Классическая игра")
        self.window.resizable(False, False)
        
        # Размеры игрового поля
        self.grid_size = 20  # размер клетки в пикселях
        self.grid_width = 30  # ширина в клетках
        self.grid_height = 20  # высота в клетках
        
        self.width = self.grid_width * self.grid_size
        self.height = self.grid_height * self.grid_size
        
        # Центрирование окна
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height - 100) // 2
        self.window.geometry(f"{self.width}x{self.height + 80}+{x}+{y}")
        
        # Игровые переменные
        self.snake = [(self.grid_width // 2, self.grid_height // 2)]
        self.direction = 'Right'  # Начальное направление
        self.next_direction = 'Right'
        self.food = self.generate_food()
        self.score = 0
        self.game_over_flag = False
        self.paused = False
        self.speed = 150  # миллисекунды между ходами
        
        # Цвета
        self.colors = {
            'bg': '#1a1a2e',
            'snake': '#00ff88',
            'snake_head': '#00cc6a',
            'food': '#ff3333',
            'grid': '#16213e',
            'text': '#ffffff'
        }
        
        # Создание интерфейса
        self.create_widgets()
        
        # Привязка клавиш
        self.bind_keys()
        
        # Запуск игры
        self.update_game()
        self.window.mainloop()
    
    def create_widgets(self):
        """Создание всех элементов интерфейса"""
        # Верхняя панель с информацией
        self.info_frame = tk.Frame(self.window, bg=self.colors['bg'], height=60)
        self.info_frame.pack(fill='x')
        
        # Отображение счёта
        self.score_label = tk.Label(
            self.info_frame,
            text=f"Счёт: {self.score}",
            font=('Arial', 18, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['bg']
        )
        self.score_label.pack(side='left', padx=20, pady=10)
        
        # Кнопка паузы
        self.pause_button = tk.Button(
            self.info_frame,
            text="⏸ Пауза",
            font=('Arial', 12, 'bold'),
            command=self.toggle_pause,
            bg='#e74c3c',
            fg='white',
            cursor='hand2',
            relief='raised',
            bd=2
        )
        self.pause_button.pack(side='right', padx=20, pady=10)
        
        # Игровое поле (Canvas)
        self.canvas = tk.Canvas(
            self.window,
            width=self.width,
            height=self.height,
            bg=self.colors['bg'],
            highlightthickness=0
        )
        self.canvas.pack()
        
        # Отображение сетки
        self.draw_grid()
        
        # Нижняя панель с управлением
        self.control_frame = tk.Frame(self.window, bg=self.colors['bg'], height=30)
        self.control_frame.pack(fill='x')
        
        controls_text = "Управление: ← ↑ ↓ → | R - новая игра | P - пауза"
        self.controls_label = tk.Label(
            self.control_frame,
            text=controls_text,
            font=('Arial', 10),
            fg='#888888',
            bg=self.colors['bg']
        )
        self.controls_label.pack(pady=5)
    
    def draw_grid(self):
        """Рисование сетки на поле"""
        for x in range(0, self.width, self.grid_size):
            self.canvas.create_line(x, 0, x, self.height, fill=self.colors['grid'], width=1)
        for y in range(0, self.height, self.grid_size):
            self.canvas.create_line(0, y, self.width, y, fill=self.colors['grid'], width=1)
    
    def bind_keys(self):
        """Привязка клавиш управления"""
        self.window.bind('<Left>', lambda e: self.change_direction('Left'))
        self.window.bind('<Right>', lambda e: self.change_direction('Right'))
        self.window.bind('<Up>', lambda e: self.change_direction('Up'))
        self.window.bind('<Down>', lambda e: self.change_direction('Down'))
        self.window.bind('<r>', lambda e: self.reset_game())
        self.window.bind('<R>', lambda e: self.reset_game())
        self.window.bind('<p>', lambda e: self.toggle_pause())
        self.window.bind('<P>', lambda e: self.toggle_pause())
        self.window.bind('<Escape>', lambda e: self.window.quit())
    
    def change_direction(self, new_direction):
        """Изменение направления движения"""
        opposite_directions = {
            'Left': 'Right',
            'Right': 'Left',
            'Up': 'Down',
            'Down': 'Up'
        }
        
        if new_direction != opposite_directions.get(self.direction):
            self.next_direction = new_direction
    
    def toggle_pause(self):
        """Пауза/возобновление игры"""
        if not self.game_over_flag:
            self.paused = not self.paused
            if self.paused:
                self.pause_button.config(text="▶ Старт", bg='#27ae60')
                self.show_pause_message()
            else:
                self.pause_button.config(text="⏸ Пауза", bg='#e74c3c')
                self.canvas.delete("pause_text")
                self.update_game()
    
    def show_pause_message(self):
        """Показать сообщение о паузе"""
        self.canvas.create_text(
            self.width // 2,
            self.height // 2,
            text="⏸ ПАУЗА ⏸\nНажмите P или кнопку Старт",
            font=('Arial', 24, 'bold'),
            fill='#ffffff',
            tags="pause_text",
            justify='center'
        )
    
    def generate_food(self):
        """Генерация еды в свободной клетке"""
        while True:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            if (x, y) not in self.snake:
                return (x, y)
    
    def move_snake(self):
        """Движение змейки"""
        if self.game_over_flag or self.paused:
            return
        
        self.direction = self.next_direction
        head = self.snake[0]
        x, y = head
        
        # Определение новой головы
        if self.direction == 'Left':
            new_head = (x - 1, y)
        elif self.direction == 'Right':
            new_head = (x + 1, y)
        elif self.direction == 'Up':
            new_head = (x, y - 1)
        elif self.direction == 'Down':
            new_head = (x, y + 1)
        
        # Проверка столкновения с едой
        if new_head == self.food:
            self.snake.insert(0, new_head)
            self.food = self.generate_food()
            self.score += 10
            self.score_label.config(text=f"Счёт: {self.score}")
            # Увеличение скорости каждые 50 очков
            if self.score % 50 == 0 and self.speed > 80:
                self.speed = max(80, self.speed - 10)
        else:
            self.snake.insert(0, new_head)
            self.snake.pop()
        
        # Проверка столкновения со стенами
        x, y = self.snake[0]
        if (x < 0 or x >= self.grid_width or 
            y < 0 or y >= self.grid_height):
            self.game_over()
        
        # Проверка столкновения с собой
        if self.snake[0] in self.snake[1:]:
            self.game_over()
    
    def draw(self):
        """Отрисовка всех элементов"""
        self.canvas.delete("all")
        self.draw_grid()
        
        # Отрисовка еды
        fx, fy = self.food
        self.canvas.create_rectangle(
            fx * self.grid_size + 2,
            fy * self.grid_size + 2,
            (fx + 1) * self.grid_size - 2,
            (fy + 1) * self.grid_size - 2,
            fill=self.colors['food'],
            outline='',
            tags="food"
        )
        
        # Отрисовка змейки
        for i, segment in enumerate(self.snake):
            x, y = segment
            color = self.colors['snake_head'] if i == 0 else self.colors['snake']
            
            # Закруглённые квадраты для змейки
            self.canvas.create_rectangle(
                x * self.grid_size + 2,
                y * self.grid_size + 2,
                (x + 1) * self.grid_size - 2,
                (y + 1) * self.grid_size - 2,
                fill=color,
                outline='',
                tags="snake"
            )
            
            # Глаза для головы
            if i == 0:
                eye_size = 3
                if self.direction == 'Right':
                    self.canvas.create_oval(
                        (x + 1) * self.grid_size - 8,
                        y * self.grid_size + 6,
                        (x + 1) * self.grid_size - 4,
                        y * self.grid_size + 10,
                        fill='white', tags="eyes"
                    )
                    self.canvas.create_oval(
                        (x + 1) * self.grid_size - 8,
                        (y + 1) * self.grid_size - 10,
                        (x + 1) * self.grid_size - 4,
                        (y + 1) * self.grid_size - 6,
                        fill='white', tags="eyes"
                    )
                elif self.direction == 'Left':
                    self.canvas.create_oval(
                        x * self.grid_size + 4,
                        y * self.grid_size + 6,
                        x * self.grid_size + 8,
                        y * self.grid_size + 10,
                        fill='white', tags="eyes"
                    )
                    self.canvas.create_oval(
                        x * self.grid_size + 4,
                        (y + 1) * self.grid_size - 10,
                        x * self.grid_size + 8,
                        (y + 1) * self.grid_size - 6,
                        fill='white', tags="eyes"
                    )
        
        # Если игра окончена, показываем сообщение
        if self.game_over_flag:
            self.canvas.create_text(
                self.width // 2,
                self.height // 2,
                text=f"💀 ИГРА ОКОНЧЕНА 💀\nСчёт: {self.score}\nНажмите R для новой игры",
                font=('Arial', 24, 'bold'),
                fill='#ff4444',
                justify='center'
            )
    
    def update_game(self):
        """Обновление игры (основной цикл)"""
        if not self.paused and not self.game_over_flag:
            self.move_snake()
            self.draw()
        
        if not self.game_over_flag and not self.paused:
            self.window.after(self.speed, self.update_game)
        elif not self.game_over_flag and self.paused:
            self.window.after(100, self.update_game)
        else:
            self.draw()
    
    def game_over(self):
        """Конец игры"""
        self.game_over_flag = True
        self.draw()
        result = messagebox.askyesno(
            "Игра окончена",
            f"💀 Game Over! 💀\nВаш счёт: {self.score}\n\nХотите сыграть ещё раз?"
        )
        if result:
            self.reset_game()
    
    def reset_game(self):
        """Сброс игры"""
        self.snake = [(self.grid_width // 2, self.grid_height // 2)]
        self.direction = 'Right'
        self.next_direction = 'Right'
        self.score = 0
        self.game_over_flag = False
        self.paused = False
        self.speed = 150
        self.score_label.config(text=f"Счёт: {self.score}")
        self.pause_button.config(text="⏸ Пауза", bg='#e74c3c')
        self.food = self.generate_food()
        self.draw()
        self.update_game()

if __name__ == "__main__":
    game = SnakeGame()