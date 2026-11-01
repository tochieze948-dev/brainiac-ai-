from agent import BrainiacAI


def main():
    """Run a simple chat loop in the terminal."""
    print("Welcome to Brainiac AI!")
    print("I can answer questions, help with tasks, and chat with you.")
    print("Type 'exit' to quit.")

    try:
        assistant = BrainiacAI()
    except ValueError as error:
        print(f"Setup issue: {error}")
        print("1. Copy .env.example to .env")
        print("2. Add your OpenAI API key to the .env file")
        print("3. Run the app again.")
        return

    while True:
        user_input = input("\nYou: ").strip()

        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit", "bye"}:
            print("Brainiac AI: Goodbye! Have a great day.")
            break

        try:
            answer = assistant.ask(user_input)
            print(f"\nBrainiac AI: {answer}")
        except Exception as error:
            print(f"\nBrainiac AI: Sorry, I ran into an error: {error}")
            print("Please check your API key and internet connection.")


if __name__ == "__main__":
    main()
