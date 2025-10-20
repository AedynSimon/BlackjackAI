import random

# --- Helper functions ---


def hand_value(hand):
    """Return the total value of a hand"""
    running_sum = 0
    ace_count = 0
    # Get total ace-high sum
    for card in hand:
        if card in ['K', 'Q', 'J']:
            running_sum += 10
        elif card == 'A':
            running_sum += 11
            ace_count += 1
        else:
            running_sum += card
    
    # Turn aces from 11's back into 1's if the current hand is over 21
    while (running_sum > 21 and ace_count > 0):
        running_sum -= 10
        ace_count -= 1

    return running_sum


def is_bust(hand):
    """Return True if the hand value exceeds 21"""
    return hand_value(hand) > 21

# --- Environment class ---


class BlackjackEnvironment:
    def __init__(self, natural=False, num_decks=6, infinite_decks = False):
        self.natural = natural  # Optional 1.5 on a "natural" Blackjack
        self.num_decks = num_decks  # Number of decks to use
        self.dealer = None  # Dealer's hand
        self.player = None  # Player's hand
        self.deck = None  # The current deck of cards
        self.true_count = 0
        self.running_count = 0

    def make_deck(self, num_decks=1):
        """Create and shuffle a shoe with the given number of decks."""
        single_deck = ['A', 2, 3, 4, 5, 6, 7, 8,
                       9, 10, 'J', 'Q', 'K'] * 4  # 52 cards
        deck = single_deck * num_decks  # Multiply by number of decks
        random.shuffle(deck)
        return deck

    def draw_card(self):
        """Draw a card"""\
        # If number of decks is infinite, draw a random card
        if (self.num_decks == -1):
            return random.choice(['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K'])

        if not self.deck:  # Reshuffle if all cards used and reset card counting
            print("Reshuffling shoe...")
            self.deck = self.make_deck(self.num_decks)
            self.running_count = 0
            self.true_count = 0

        card = self.deck.pop()

        self.update_count(card)

        return card
    

    # Card counting with a true count
    def update_count(self, card):
        if card in {'J', 'Q', 'K', 'A', 10}:
            self.running_count -= 1
        elif (card >= 2) and (card <= 6):
            self.running_count += 1

        self.true_count = self.running_count / (max((len(self.deck) / 52), 1e-6))

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
        """Observation = (player_sum, dealer_showing)"""
        return (
            hand_value(self.player),
            self.dealer[0],
            self.true_count
        )

    def step(self, action):
        """
        Take an action in the environment.
        action: 
            0 = stand
            1 = hit
        """
        # Hit
        if action == 1:
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
