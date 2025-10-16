import random

# --- Helper functions ---


def hand_value(hand):
    """Return the total value of a hand"""
    return sum(hand)


def is_bust(hand):
    """Return True if the hand value exceeds 21"""
    return hand_value(hand) > 21


def has_ace(hand):
    """Check if hand has any ace(s)"""
    if 1 in hand or 11 in hand:
        return True
    return False


def ace_mode(hand):
    """Return True if any ace in hand is currently 11"""
    for card in hand:
        if card == 11:
            return True
    return False


# --- Environment class ---


class BlackjackEnvironment:
    def __init__(self, natural=False, num_decks=8):
        self.natural = natural  # Optional 1.5 on a "natural" Blackjack
        self.num_decks = num_decks  # Number of decks to use
        self.dealer = None  # Dealer's hand
        self.player = None  # Player's hand
        self.deck = None  # The current deck of cards

    def make_deck(self, num_decks=1):
        """Create and shuffle a shoe with the given number of decks."""
        single_deck = [1, 2, 3, 4, 5, 6, 7, 8,
                       9, 10, 10, 10, 10] * 4  # 52 cards
        deck = single_deck * num_decks  # Multiply by number of decks
        random.shuffle(deck)
        return deck

    def draw_card(self):
        """Draw a card: 1 = Ace, 2-10 = face value, 10 = Jack/Queen/King"""
        if not self.deck:  # Reshuffle if all cards used
            print("Reshuffling shoe...")
            self.deck = self.make_deck(self.num_decks)
        return self.deck.pop()

    def draw_hand(self):
        """Draw two cards to form a hand"""
        return [self.draw_card(), self.draw_card()]

    def reset(self):
        """Start a new round (reshuffle and deal initial hands)"""
        self.deck = self.make_deck(self.num_decks)  # Freshly shuffled shoe
        self.dealer = self.draw_hand()  # Dealer’s initial two cards
        self.player = self.draw_hand()  # Player’s initial two cards
        return self.observation()

    def observation(self):
        """Observation = (player_sum, dealer_showing, has_ace, ace_mode)"""
        return (
            hand_value(self.player),
            self.dealer[0],
            has_ace(self.player),
            ace_mode(self.player)
        )

    def step(self, action):
        """
        Take an action in the environment.
        action: 
          0 = stand
          1 = hit
          2 = toggle_ace (switch one Ace between 1 and 11)
        """
        # Toggle ace value
        if action == 2:
            for i, card in enumerate(self.player):
                if card == 1:
                    self.player[i] = 11
                    break
                elif card == 11:
                    self.player[i] = 1
                    break
            return self.observation(), 0, False, {}

        # Hit
        elif action == 1:
            self.player.append(self.draw_card())
            if is_bust(self.player):
                # Player busts immediate loss
                return self.observation(), -1, True, {}
            else:
                # Still in the game
                return self.observation(), 0, False, {}

        # Stand
        else:
            # Dealer draws until reaching 17 or higher
            while hand_value(self.dealer) < 17:
                self.dealer.append(self.draw_card())
            # Compare hands and calculate result
            reward = self.compare()
            return self.observation(), reward, True, {}

    def compare(self):
        """Compare player and dealer hands and return the game outcome."""
        player_value = hand_value(self.player)
        dealer_value = hand_value(self.dealer)

        if is_bust(self.dealer):
            return +1  # Dealer busts player wins
        elif player_value > dealer_value:
            return +1  # Player closer to 21 win
        elif player_value < dealer_value:
            return -1  # Dealer closer to 21 lose
        else:
            return 0  # Push (tie)

    def display(self, reveal=False):
        """Display current hands; hide dealer's hole card until reveal=True."""
        if reveal:
            # Show dealer’s full hand and total (after game ends)
            print(f"Dealer: {self.dealer} ({hand_value(self.dealer)})")
        else:
            # Show only the dealer’s first card
            print(f"Dealer: [{self.dealer[0]}, '?']")

        print(f"Player: {self.player} ({hand_value(self.player)})")
