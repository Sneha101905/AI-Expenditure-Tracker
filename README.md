# AI Expenditure Tracker
A Python command-line tool to log, view, and analyze personal spending, extended with an AI-powered natural language interface via the Gemini API.
Ask questions like "How much did I spend on food last month?" or "Where can I cut back?" and get answers from your expense data.
Built as the final project for [HarvardX CS50P](https://cs50.harvard.edu/python/), then extended with an LLM-powered chat feature.
## Features
- Add expenses with amount, category, description, and date
- View a full expense history in a formatted table
- Analyze spending by category with percentages and totals
- Chat with your expenses in plain English using Gemini (Google AI API)
## Setup
**1. Clone the repository**
```bash
git clone https://github.com/Sneha101905/ai-expenditure-tracker.git
cd ai-expenditure-tracker
```
**2. Install dependencies**
```bash
pip install google-generativeai
```
**3. Get a Gemini API key**
Sign up at [aistudio.google.com](https://aistudio.google.com) and create an API key. You can either paste it when prompted by the program, or set it as an environment variable:
```bash
export GEMINI_API_KEY="your-key-here"
```
**4. Run the tracker**
```bash
python project_personal.py
```
## How it works
Expenses are stored locally in an `expenses.csv` file. When you open the AI chat (option 4), your complete expense history is formatted and sent to Gemini as context alongside your question. The model reasons over your real data to generate answers.
Conversation history is maintained within each session, so follow-up questions work naturally.
## Example chat session
```
=== AI Expense Chat ===
Ask anything about your spending. Type 'quit' to exit.
You: How much have I spent on food total?
Assistant: Based on your expense history, you've spent $284.50 on Food across 9 entries.
You: Which month was the most expensive?
Assistant: March was your highest-spending month at $412.00, driven largely by Shopping and Bills.
You: Where can I cut back?
Assistant: Entertainment appears most frequently relative to its necessity — 6 entries totaling $138.00.
You might also review the 3 "Other" entries ($97.50) which lack descriptions, making them harder to evaluate.
```
---
## Project structure
```
├── project_personal.py   # Main program with AI chat integration
├── project.py            # Original CS50P submission
├── test_project.py       # Unit tests
├── requirements.txt      # Dependencies
└── expenses.csv          # Auto-generated on first expense entry
```
---
## Technologies used
- Python 3
- [Google Generative AI Python SDK](https://github.com/google/generative-ai-python)
- Gemini (gemini-1.5-flash)
- CSV for local data storage
