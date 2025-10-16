from environment import BlackjackEnvironment


def main():
    print("Welcome to Blackjack!")
    print("Actions: [0] Stand, [1] Hit, [2] Toggle Ace\n")

    # Ask user how many decks to use
    while True:
        try:
            num_decks = int(
                input("How many decks do you want to play with? (1–8): "))
            if 1 <= num_decks <= 8:
                break
            print("Please choose a number between 1 and 8.")
        except ValueError:
            print("Please enter a valid number.")

    # Create the environment using that number of decks
    env = BlackjackEnvironment(num_decks=num_decks)

    while True:  # Loop to allow multiple games
        obs = env.reset()
        done = False

        print(
            f"\n--- New Round ({num_decks} deck{'s' if num_decks > 1 else ''}) ---")
        env.display(reveal=False)

        # Main gameplay loop
        while not done:
            try:
                action = int(
                    input("Choose action (0=stand, 1=hit, 2=toggle ace): "))
                if action not in [0, 1, 2]:
                    print("Invalid action. Please enter 0, 1, or 2.")
                    continue
            except ValueError:
                print("Please enter a valid number.")
                continue

            obs, reward, done, info = env.step(action)
            env.display(reveal=False)

            if done:
                env.display(reveal=True)
                if reward > 0:
                    print("You win!")
                elif reward < 0:
                    print("You lose!")
                else:
                    print("It's a tie!")

        # Ask if player wants to play again
        again = input("\nPlay again? (y/n): ").lower()
        if again != "y":
            print("\nThanks for playing! Goodbye.")
            break


if __name__ == "__main__":
    main()
