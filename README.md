# Brainiac AI

Brainiac AI is a simple personal AI assistant made for beginners. It can:

- chat with users in a terminal
- connect to an AI model through an API
- answer questions and help with daily tasks
- stay easy to understand and edit

## What this project includes

- `brainiac.py` - the main script that starts the chat
- `agent.py` - the logic that sends messages to the AI model
- `config.py` - loads settings from a `.env` file
- `.env.example` - example environment file with placeholder values
- `requirements.txt` - Python packages needed for the app

## Requirements

Before you begin, make sure you have:

- Python 3.10 or newer installed
- access to an OpenAI-compatible API key

## Step 1: Install Python dependencies

Open your terminal in the project folder and run:

```bash
pip install -r requirements.txt
```

## Step 2: Set up your environment file

Create a copy of the example file:

```bash
cp .env.example .env
```

Now open `.env` and replace the placeholder with your real API key.

Example:

```env
OPENAI_API_KEY=your_actual_api_key_here
MODEL_NAME=gpt-4o-mini
```

Important:
- never share your API key in public code repositories
- never commit your real `.env` file

## Step 3: Run the app

Start the assistant with:

```bash
python brainiac.py
```

You will see a chat prompt like this:

```text
You: Hello Brainiac AI!
Brainiac AI: Hello! How can I help you today?
```

Type your message and press Enter.

To exit the app, type:

```text
exit
```

## Beginner note

This project is intentionally simple so you can learn the basics of:

- Python scripts
- environment variables
- API connections
- terminal-based chat apps

If you want to improve it later, you could add:

- a web interface
- saved chat history
- task automation
- voice input/output

## Important security note

- Do not put real API keys or passwords in source code.
- Use `.env` for local secrets only.
- Keep `.env` out of version control.
