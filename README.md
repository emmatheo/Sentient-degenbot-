# 🤖 Sentient DegenChat v2 Bot

An AI-powered Telegram bot built on **Sentient’s Dobby model**, designed to chat, educate, and entertain the crypto community.  
This version is lightweight (<200 lines) and beginner-friendly — perfect for Replit or Render deployment.

---

## 🚀 Features

| Command | Description | Example |
|----------|--------------|----------|
| `/start` | Initialize chat and set default mode to `degen` | `/start` |
| `/help` | List all available commands | `/help` |
| `/trend <TOKEN>` | Get on-chain + sentiment summary of any token | `/trend SOL` |
| `/explain <TERM>` | Explain a crypto concept in simple terms | `/explain restaking` |
| `/meme` | Generate a short crypto meme caption | `/meme` |
| `/alpha` | Share a quick short-term market prediction | `/alpha` |
| `/mode <degen|tutor|analyst>` | Switch bot personality modes | `/mode tutor` |

---

## 🧠 Personality Modes

- **Degen** — witty, funny, market-savvy, slang-filled.
- **Tutor** — calm, friendly explainer for beginners.
- **Analyst** — concise, professional, on-chain focused.

Each chat can switch between these personalities using `/mode`.

---

## ⚙️ Tech Stack

- **Language:** Python  
- **Framework:** [python-telegram-bot 20.x](https://python-telegram-bot.org)  
- **AI Model:** Sentient `dobby`  
- **API Calls:** Sentient API (Chat Completion endpoint)  
- **Hosting:** Replit, Render, or any Python environment

---

## 📂 Project Structure

# Sentient-degenbot-


---

## 🔒 Environment Variables

| Variable | Description | Example |
|-----------|--------------|----------|
| `TELEGRAM_TOKEN` | Telegram BotFather token | `123456:ABC-xyz` |
| `SENTIENT_API_KEY` | Your Sentient API key | `sk-xxxx` |
| `SENTIENT_API_URL` | (optional) API endpoint | `https://api.sentient.ai/v1/chat/completions` |
| `SENTIENT_MODEL` | (optional) model name | `dobby` |

> ⚠️ Never hardcode your API keys.  
> Use Replit Secrets or `.env` files for safety.

---

## 🧩 Installation & Setup

### Option 1: Run on Replit
1. Create a new **Python Repl**.
2. Paste all code from `main.py`.
3. Add your secrets under the **🔒 “Secrets”** tab:
   - `TELEGRAM_TOKEN`
   - `SENTIENT_API_KEY`
4. Add dependencies in the shell or Packages tab:
5. 5. Press **Run** — your bot is live!

### Option 2: Local / Render
```bash
git clone https://github.com/<yourusername>/DegenChat-v2.git
cd DegenChat-v2
pip install -r requirements.txt
export TELEGRAM_TOKEN=your_token
export SENTIENT_API_KEY=your_key
python main.py
