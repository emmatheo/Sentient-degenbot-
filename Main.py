import os, requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# 🔑 Env vars (set these in Replit Secrets)
SENTIENT_API_KEY = os.getenv("SENTIENT_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
SENTIENT_MODEL = os.getenv("SENTIENT_MODEL", "dobby")
SENTIENT_API_URL = os.getenv("SENTIENT_API_URL", "https://api.sentient.ai/v1/chat/completions")

# Store mode per chat in memory
chat_modes = {}

# --- Helpers ---
def call_sentient(prompt, max_tokens=200):
    headers = {"Authorization": f"Bearer {SENTIENT_API_KEY}", "Content-Type": "application/json"}
    data = {"model": SENTIENT_MODEL, "messages": [{"role": "user", "content": prompt}], "max_tokens": max_tokens}
    res = requests.post(SENTIENT_API_URL, json=data, headers=headers, timeout=30)
    res.raise_for_status()
    return res.json()["choices"][0]["message"]["content"].strip()

def prefix(mode):
    if mode == "tutor":
        return "You are a calm crypto tutor, explain simply."
    if mode == "analyst":
        return "You are a concise on-chain analyst."
    return "You are a witty, slightly degen crypto AI."

# --- Commands ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_modes[update.effective_chat.id] = "degen"
    await update.message.reply_text("⚡ DegenChat v2 online — use /help to see commands")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = (
        "/trend <TOKEN> — market mood\n"
        "/explain <TERM> — explain simply\n"
        "/meme — crypto meme caption\n"
        "/alpha — short prediction\n"
        "/mode <degen|tutor|analyst>\n"
        "/help — show this list"
    )
    await update.message.reply_text(txt)

async def mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if not context.args:
        m = chat_modes.get(chat_id, "degen")
        await update.message.reply_text(f"Current mode: {m}")
        return
    mode = context.args[0].lower()
    if mode not in ["degen", "tutor", "analyst"]:
        await update.message.reply_text("Modes: degen, tutor, analyst")
        return
    chat_modes[chat_id] = mode
    await update.message.reply_text(f"Mode set to {mode}")

async def trend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    token = " ".join(context.args)
    if not token: 
        await update.message.reply_text("Usage: /trend SOL")
        return
    mode = chat_modes.get(update.effective_chat.id, "degen")
    prompt = f"{prefix(mode)}\nGive 3-line on-chain & sentiment trend for {token} with 1 risk note."
    await update.message.reply_text("Thinking...")
    try: await update.message.reply_text(call_sentient(prompt))
    except Exception as e: await update.message.reply_text(f"Error: {e}")

async def explain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    term = " ".join(context.args)
    if not term:
        await update.message.reply_text("Usage: /explain restaking")
        return
    mode = chat_modes.get(update.effective_chat.id, "degen")
    prompt = f"{prefix(mode)}\nExplain '{term}' simply with 1 example and short takeaway."
    try: await update.message.reply_text(call_sentient(prompt))
    except Exception as e: await update.message.reply_text(f"Error: {e}")

async def meme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = chat_modes.get(update.effective_chat.id, "degen")
    prompt = f"{prefix(mode)}\nWrite a funny crypto meme caption (1-2 lines, no profanity)."
    try: await update.message.reply_text(call_sentient(prompt, 60))
    except Exception as e: await update.message.reply_text(f"Error: {e}")

async def alpha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = chat_modes.get(update.effective_chat.id, "degen")
    prompt = f"{prefix(mode)}\nGive 2-line spicy short-term alpha for a random token + 1 risk."
    try: await update.message.reply_text(call_sentient(prompt, 100))
    except Exception as e: await update.message.reply_text(f"Error: {e}")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    mode = chat_modes.get(update.effective_chat.id, "degen")
    prompt = f"{prefix(mode)}\nUser: {text}\nReply briefly and witty."
    try: await update.message.reply_text(call_sentient(prompt, 150))
    except Exception as e: await update.message.reply_text(f"Error: {e}")

# --- Run bot ---
def main():
    if not TELEGRAM_TOKEN or not SENTIENT_API_KEY:
        raise SystemExit("Missing TELEGRAM_TOKEN or SENTIENT_API_KEY in environment!")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("mode", mode))
    app.add_handler(CommandHandler("trend", trend))
    app.add_handler(CommandHandler("explain", explain))
    app.add_handler(CommandHandler("meme", meme))
    app.add_handler(CommandHandler("alpha", alpha))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()

if __name__ == "__main__":
    main()
