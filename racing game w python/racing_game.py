import tkinter as tk
from tkinter import messagebox
import random

class RacingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("CAR RACING")
        self.root.configure(bg="#2c3e50")
        self.root.resizable(False, False)

        # Game settings
        self.width = 400
        self.height = 600
        self.car_width = 40
        self.car_height = 60
        self.enemy_width = 40
        self.enemy_height = 60

        # Colors
        self.road_color = "#4a4a4a"
        self.line_color = "#ffff00"
        self.grass_color = "#2ecc71"

        # Game state
        self.car_x = self.width // 2 - self.car_width // 2
        self.car_y = self.height - 100
        self.car_speed = 15

        self.enemies = []
        self.enemy_speed = 5

        self.lines = []
        self.line_speed = 8

        self.score = 0
        self.high_score = 0
        self.level = 1
        self.game_running = False

        self.build_ui()

    def build_ui(self):
        """Build the game UI"""
        # Main frame
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(padx=20, pady=20)

        # Title
        title = tk.Label(
            main_frame,
            text="CAR RACING",
            font=("Arial", 32, "bold"),
            bg="#2c3e50",
            fg="#e74c3c"
        )
        title.pack(pady=10)

        # Score panel
        score_frame = tk.Frame(main_frame, bg="#34495e", relief=tk.RAISED, borderwidth=3)
        score_frame.pack(fill=tk.X, pady=10)

        # Score info
        info_frame = tk.Frame(score_frame, bg="#34495e")
        info_frame.pack(pady=10)

        self.score_label = tk.Label(
            info_frame,
            text=f"SCORE: {self.score}",
            font=("Arial", 14, "bold"),
            bg="#34495e",
            fg="#f39c12"
        )
        self.score_label.pack(side=tk.LEFT, padx=15)

        self.high_score_label = tk.Label(
            info_frame,
            text=f"HIGH SCORE: {self.high_score}",
            font=("Arial", 14, "bold"),
            bg="#34495e",
            fg="#3498db"
        )
        self.high_score_label.pack(side=tk.LEFT, padx=15)

        self.level_label = tk.Label(
            info_frame,
            text=f"LEVEL: {self.level}",
            font=("Arial", 14, "bold"),
            bg="#34495e",
            fg="#2ecc71"
        )
        self.level_label.pack(side=tk.LEFT, padx=15)

        # Canvas (game area)
        self.canvas = tk.Canvas(
            main_frame,
            width=self.width,
            height=self.height,
            bg=self.road_color,
            highlightthickness=3,
            highlightbackground="#e74c3c"
        )
        self.canvas.pack()

        # Grass edges
        self.canvas.create_rectangle(
            0, 0, 50, self.height,
            fill=self.grass_color, outline=""
        )
        self.canvas.create_rectangle(
            self.width - 50, 0, self.width, self.height,
            fill=self.grass_color, outline=""
        )

        # Build road lines
        self.build_road_lines()

        # Player's car
        self.car = self.build_car(self.car_x, self.car_y, "#e74c3c")

        # Controls info
        controls_label = tk.Label(
            main_frame,
            text="ARROW KEYS: LEFT/RIGHT  |  SPACE: START  |  ESC: QUIT",
            font=("Arial", 11),
            bg="#2c3e50",
            fg="#95a5a6"
        )
        controls_label.pack(pady=10)

        # Start message
        self.message_text = self.canvas.create_text(
            self.width // 2,
            self.height // 2,
            text="PRESS SPACE\nTO START",
            font=("Arial", 20, "bold"),
            fill="white",
            justify=tk.CENTER
        )

        # Keyboard controls
        self.root.bind("<Left>", lambda e: self.move("Left"))
        self.root.bind("<Right>", lambda e: self.move("Right"))
        self.root.bind("<space>", lambda e: self.start_game())
        self.root.bind("<Escape>", lambda e: self.root.quit())

        # A and D keys (alternative)
        self.root.bind("a", lambda e: self.move("Left"))
        self.root.bind("d", lambda e: self.move("Right"))

    def build_car(self, x, y, color):
        """Build a car shape"""
        car_parts = []

        # Body
        body = self.canvas.create_rectangle(
            x, y, x + self.car_width, y + self.car_height,
            fill=color, outline="black", width=2
        )
        car_parts.append(body)

        # Front windshield
        windshield = self.canvas.create_rectangle(
            x + 5, y + 10, x + self.car_width - 5, y + 25,
            fill="#87ceeb", outline="black", width=1
        )
        car_parts.append(windshield)

        # Rear window
        rear_window = self.canvas.create_rectangle(
            x + 5, y + 35, x + self.car_width - 5, y + 50,
            fill="#87ceeb", outline="black", width=1
        )
        car_parts.append(rear_window)

        return car_parts

    def build_road_lines(self):
        """Build the road lane lines"""
        line_count = 10
        line_height = 40
        gap = 40

        for i in range(line_count):
            y = i * (line_height + gap) - 300
            line = self.canvas.create_rectangle(
                self.width // 2 - 3,
                y,
                self.width // 2 + 3,
                y + line_height,
                fill=self.line_color,
                outline=""
            )
            self.lines.append(line)

    def spawn_enemy(self):
        """Spawn an enemy car"""
        # Pick a random lane (3 lanes)
        lanes = [70, 180, 290]
        x = random.choice(lanes)
        y = -self.enemy_height

        colors = ["#3498db", "#9b59b6", "#f39c12", "#1abc9c", "#34495e"]
        color = random.choice(colors)

        enemy = self.build_car(x, y, color)
        self.enemies.append({"parts": enemy, "x": x, "y": y})

    def start_game(self):
        """Start the game"""
        if not self.game_running:
            self.game_running = True
            self.canvas.delete(self.message_text)
            self.game_loop()

    def move(self, direction):
        """Move the player's car"""
        if not self.game_running:
            return

        if direction == "Left" and self.car_x > 60:
            self.car_x -= self.car_speed
            for part in self.car:
                self.canvas.move(part, -self.car_speed, 0)

        elif direction == "Right" and self.car_x < self.width - 50 - self.car_width:
            self.car_x += self.car_speed
            for part in self.car:
                self.canvas.move(part, self.car_speed, 0)

    def move_road_lines(self):
        """Move the road lines downward"""
        for line in self.lines:
            coords = self.canvas.coords(line)
            if coords[1] > self.height:
                self.canvas.move(line, 0, -800)
            else:
                self.canvas.move(line, 0, self.line_speed)

    def move_enemies(self):
        """Move enemy cars"""
        for enemy in self.enemies[:]:
            enemy["y"] += self.enemy_speed

            # Move the enemy
            for part in enemy["parts"]:
                self.canvas.move(part, 0, self.enemy_speed)

            # If it went off screen, remove it and add score
            if enemy["y"] > self.height:
                for part in enemy["parts"]:
                    self.canvas.delete(part)
                self.enemies.remove(enemy)
                self.add_score()

    def check_collision(self):
        """Check for collisions"""
        for enemy in self.enemies:
            dx = enemy["x"]
            dy = enemy["y"]

            # Simple collision detection
            if (self.car_x < dx + self.enemy_width and
                self.car_x + self.car_width > dx and
                self.car_y < dy + self.enemy_height and
                self.car_y + self.car_height > dy):
                return True
        return False

    def add_score(self):
        """Add to the score"""
        self.score += 10
        self.score_label.config(text=f"SCORE: {self.score}")

        # Level up
        if self.score % 100 == 0:
            self.level += 1
            self.level_label.config(text=f"LEVEL: {self.level}")
            self.enemy_speed += 1
            self.line_speed += 1

    def end_game(self):
        """End the game"""
        self.game_running = False

        # Update the high score
        if self.score > self.high_score:
            self.high_score = self.score
            self.high_score_label.config(text=f"HIGH SCORE: {self.high_score}")

        # Game over message
        self.message_text = self.canvas.create_text(
            self.width // 2,
            self.height // 2,
            text=f"GAME OVER!\n\nSCORE: {self.score}\n\nPRESS SPACE\nFOR A NEW GAME",
            font=("Arial", 18, "bold"),
            fill="white",
            justify=tk.CENTER
        )

        # Clear enemies
        for enemy in self.enemies:
            for part in enemy["parts"]:
                self.canvas.delete(part)
        self.enemies.clear()

        # Reset state
        self.score = 0
        self.level = 1
        self.enemy_speed = 5
        self.line_speed = 8

        self.score_label.config(text=f"SCORE: {self.score}")
        self.level_label.config(text=f"LEVEL: {self.level}")

        # Move the car back to the starting position
        dx = (self.width // 2 - self.car_width // 2) - self.car_x
        for part in self.car:
            self.canvas.move(part, dx, 0)
        self.car_x = self.width // 2 - self.car_width // 2

    def game_loop(self):
        """Main game loop"""
        if not self.game_running:
            return

        # Move the road lines
        self.move_road_lines()

        # Spawn an enemy (randomly)
        if random.randint(1, 30) == 1:
            self.spawn_enemy()

        # Move enemies
        self.move_enemies()

        # Check for collisions
        if self.check_collision():
            self.end_game()
            return

        # Repeat the loop
        self.root.after(50, self.game_loop)


if __name__ == "__main__":
    root = tk.Tk()
    game = RacingGame(root)
    root.mainloop()
