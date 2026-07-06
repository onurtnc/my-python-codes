import tkinter as tk
from tkinter import messagebox
import random

class Blackjack:
    def __init__(self, root):
        self.root = root
        self.root.title("BLACKJACK (21)")
        self.root.geometry("800x700")
        self.root.configure(bg="#1a5f3f")
        self.root.resizable(False, False)

        # Game state
        self.deck = []
        self.player_cards = []
        self.dealer_cards = []
        self.player_score = 0
        self.dealer_score = 0
        self.money = 1000
        self.bet = 0
        self.game_over = False

        # Card symbols
        self.suits = ['S', 'H', 'D', 'C']
        self.values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

        self.build_ui()
        self.new_game()

    def build_ui(self):
        """Build the game UI"""
        # Title
        title = tk.Label(
            self.root,
            text="BLACKJACK (21)",
            font=("Arial", 28, "bold"),
            bg="#1a5f3f",
            fg="gold"
        )
        title.pack(pady=20)

        # Money and bet info
        self.info_frame = tk.Frame(self.root, bg="#1a5f3f")
        self.info_frame.pack(pady=10)

        self.money_label = tk.Label(
            self.info_frame,
            text=f"Money: ${self.money}",
            font=("Arial", 16, "bold"),
            bg="#1a5f3f",
            fg="white"
        )
        self.money_label.pack(side=tk.LEFT, padx=20)

        self.bet_label = tk.Label(
            self.info_frame,
            text=f"Bet: ${self.bet}",
            font=("Arial", 16, "bold"),
            bg="#1a5f3f",
            fg="yellow"
        )
        self.bet_label.pack(side=tk.LEFT, padx=20)

        # Dealer's cards area
        dealer_title = tk.Label(
            self.root,
            text="DEALER",
            font=("Arial", 18, "bold"),
            bg="#1a5f3f",
            fg="white"
        )
        dealer_title.pack(pady=5)

        self.dealer_frame = tk.Frame(self.root, bg="#1a5f3f")
        self.dealer_frame.pack(pady=10)

        self.dealer_score_label = tk.Label(
            self.root,
            text="Score: ?",
            font=("Arial", 14),
            bg="#1a5f3f",
            fg="white"
        )
        self.dealer_score_label.pack()

        # Player's cards area
        player_title = tk.Label(
            self.root,
            text="YOU",
            font=("Arial", 18, "bold"),
            bg="#1a5f3f",
            fg="white"
        )
        player_title.pack(pady=5)

        self.player_frame = tk.Frame(self.root, bg="#1a5f3f")
        self.player_frame.pack(pady=10)

        self.player_score_label = tk.Label(
            self.root,
            text="Score: 0",
            font=("Arial", 14),
            bg="#1a5f3f",
            fg="white"
        )
        self.player_score_label.pack()

        # Bet input
        bet_frame = tk.Frame(self.root, bg="#1a5f3f")
        bet_frame.pack(pady=15)

        tk.Label(
            bet_frame,
            text="Bet Amount:",
            font=("Arial", 12),
            bg="#1a5f3f",
            fg="white"
        ).pack(side=tk.LEFT, padx=5)

        self.bet_entry = tk.Entry(bet_frame, font=("Arial", 12), width=10)
        self.bet_entry.pack(side=tk.LEFT, padx=5)
        self.bet_entry.insert(0, "50")

        # Buttons
        button_frame = tk.Frame(self.root, bg="#1a5f3f")
        button_frame.pack(pady=10)

        self.bet_button = tk.Button(
            button_frame,
            text="PLACE BET",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            width=12,
            command=self.place_bet
        )
        self.bet_button.pack(side=tk.LEFT, padx=5)

        self.hit_button = tk.Button(
            button_frame,
            text="HIT",
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white",
            width=12,
            command=self.hit,
            state=tk.DISABLED
        )
        self.hit_button.pack(side=tk.LEFT, padx=5)

        self.stand_button = tk.Button(
            button_frame,
            text="STAND",
            font=("Arial", 12, "bold"),
            bg="#FF9800",
            fg="white",
            width=12,
            command=self.stand,
            state=tk.DISABLED
        )
        self.stand_button.pack(side=tk.LEFT, padx=5)

        self.new_game_button = tk.Button(
            button_frame,
            text="NEW GAME",
            font=("Arial", 12, "bold"),
            bg="#9C27B0",
            fg="white",
            width=12,
            command=self.new_game
        )
        self.new_game_button.pack(side=tk.LEFT, padx=5)

        # Message area
        self.message_label = tk.Label(
            self.root,
            text="Place a bet to start the game!",
            font=("Arial", 14, "bold"),
            bg="#1a5f3f",
            fg="yellow"
        )
        self.message_label.pack(pady=10)

    def build_deck(self):
        """Build a new deck of cards"""
        self.deck = []
        for suit in self.suits:
            for value in self.values:
                self.deck.append(f"{value}{suit}")
        random.shuffle(self.deck)

    def card_value(self, card):
        """Calculate the value of a card"""
        value = card[:-1]  # Last character is the suit
        if value in ['J', 'Q', 'K']:
            return 10
        elif value == 'A':
            return 11  # Ace starts at 11, adjusted to 1 if needed
        else:
            return int(value)

    def calculate_score(self, cards):
        """Calculate the score of a hand"""
        score = 0
        ace_count = 0

        for card in cards:
            value = self.card_value(card)
            score += value
            if card[:-1] == 'A':
                ace_count += 1

        # Adjust aces (count as 1 instead of 11 if over 21)
        while score > 21 and ace_count > 0:
            score -= 10
            ace_count -= 1

        return score

    def show_cards(self, frame, cards, hidden=False):
        """Display cards on screen"""
        # Clear old cards
        for widget in frame.winfo_children():
            widget.destroy()

        # Display new cards
        for i, card in enumerate(cards):
            if hidden and i == 0:
                # Hide the dealer's first card
                card_label = tk.Label(
                    frame,
                    text="[?]",
                    font=("Arial", 48),
                    bg="#1a5f3f",
                    fg="white"
                )
            else:
                # Determine card color
                if card[-1] in ['H', 'D']:
                    color = "red"
                else:
                    color = "black"

                card_label = tk.Label(
                    frame,
                    text=card,
                    font=("Arial", 36),
                    bg="white",
                    fg=color,
                    width=3,
                    height=2,
                    relief=tk.RAISED,
                    borderwidth=3
                )
            card_label.pack(side=tk.LEFT, padx=5)

    def place_bet(self):
        """Place a bet and start the round"""
        try:
            bet = int(self.bet_entry.get())

            if bet <= 0:
                messagebox.showerror("Error", "Bet must be greater than 0!")
                return

            if bet > self.money:
                messagebox.showerror("Error", "Insufficient balance!")
                return

            self.bet = bet
            self.money -= bet
            self.bet_label.config(text=f"Bet: ${self.bet}")
            self.money_label.config(text=f"Money: ${self.money}")

            # Start the round
            self.start_round()

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid bet amount!")

    def start_round(self):
        """Start a new round"""
        self.build_deck()
        self.player_cards = []
        self.dealer_cards = []
        self.game_over = False

        # Deal the initial cards
        self.player_cards.append(self.deck.pop())
        self.dealer_cards.append(self.deck.pop())
        self.player_cards.append(self.deck.pop())
        self.dealer_cards.append(self.deck.pop())

        # Calculate scores
        self.player_score = self.calculate_score(self.player_cards)
        self.dealer_score = self.calculate_score(self.dealer_cards)

        # Display cards
        self.show_cards(self.player_frame, self.player_cards)
        self.show_cards(self.dealer_frame, self.dealer_cards, hidden=True)

        # Update scores
        self.player_score_label.config(text=f"Score: {self.player_score}")
        self.dealer_score_label.config(text="Score: ?")

        # Enable/disable buttons
        self.bet_button.config(state=tk.DISABLED)
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)

        self.message_label.config(text="Hit or stand!")

        # Check for blackjack
        if self.player_score == 21:
            self.message_label.config(text="BLACKJACK!")
            self.end_round()

    def hit(self):
        """Player draws a card"""
        if self.game_over:
            return

        self.player_cards.append(self.deck.pop())
        self.player_score = self.calculate_score(self.player_cards)

        self.show_cards(self.player_frame, self.player_cards)
        self.player_score_label.config(text=f"Score: {self.player_score}")

        if self.player_score > 21:
            self.message_label.config(text="BUST! You went over 21!")
            self.end_round()
        elif self.player_score == 21:
            self.stand()

    def stand(self):
        """Player stands, dealer plays"""
        if self.game_over:
            return

        # Reveal the dealer's cards
        self.show_cards(self.dealer_frame, self.dealer_cards)
        self.dealer_score_label.config(text=f"Score: {self.dealer_score}")

        # Dealer draws until reaching 17
        while self.dealer_score < 17:
            self.root.update()
            self.root.after(500)  # Wait for animation

            self.dealer_cards.append(self.deck.pop())
            self.dealer_score = self.calculate_score(self.dealer_cards)

            self.show_cards(self.dealer_frame, self.dealer_cards)
            self.dealer_score_label.config(text=f"Score: {self.dealer_score}")

        self.end_round()

    def end_round(self):
        """End the round and determine the winner"""
        self.game_over = True

        # Reveal all of the dealer's cards
        self.show_cards(self.dealer_frame, self.dealer_cards)
        self.dealer_score_label.config(text=f"Score: {self.dealer_score}")

        # Determine the winner
        if self.player_score > 21:
            message = "BUST! You lost!"
            winnings = 0
        elif self.dealer_score > 21:
            message = "YOU WIN! Dealer busted!"
            winnings = self.bet * 2
        elif self.player_score > self.dealer_score:
            message = "YOU WIN!"
            winnings = self.bet * 2
        elif self.player_score < self.dealer_score:
            message = "YOU LOSE!"
            winnings = 0
        else:
            message = "PUSH (tie)!"
            winnings = self.bet

        # Blackjack bonus
        if self.player_score == 21 and len(self.player_cards) == 2:
            message = "BLACKJACK! 1.5x payout!"
            winnings = int(self.bet * 2.5)

        self.money += winnings

        self.message_label.config(text=message)
        self.money_label.config(text=f"Money: ${self.money}")

        # Update buttons
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.bet_button.config(state=tk.NORMAL)

        # Out of money?
        if self.money <= 0:
            messagebox.showinfo("Game Over", "You're out of money! Resetting the game...")
            self.money = 1000
            self.money_label.config(text=f"Money: ${self.money}")

    def new_game(self):
        """Start a new game"""
        self.player_cards = []
        self.dealer_cards = []
        self.bet = 0
        self.game_over = False

        # Clear cards
        for widget in self.player_frame.winfo_children():
            widget.destroy()
        for widget in self.dealer_frame.winfo_children():
            widget.destroy()

        # Reset scores
        self.player_score_label.config(text="Score: 0")
        self.dealer_score_label.config(text="Score: ?")
        self.bet_label.config(text="Bet: $0")

        # Update buttons
        self.bet_button.config(state=tk.NORMAL)
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)

        self.message_label.config(text="Place a bet to start the game!")


if __name__ == "__main__":
    root = tk.Tk()
    game = Blackjack(root)
    root.mainloop()
