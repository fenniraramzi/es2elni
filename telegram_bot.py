import logging
import os
from telegram import Update,ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import openai
from googlesearch import search

TELEGRAM_API_KEY = "5982704300:AAEuF5RZVnYwQsrw19wfqo6E_arUGfXn9wA"
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! I'm a bot powered by GPT and Google Search. Send me any question, or use /search to perform a Google search.")

def gpt_answer(update: Update, context: CallbackContext):
    query = update.message.text
    logger.debug(f"Received question: {query}")

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=query,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )

    answer = response.choices[0].text.strip()

    if not answer:
        answer = "I'm sorry, I don't have an answer for that question."

    update.message.reply_text(answer)

def google_search(update: Update, context: CallbackContext):
    query = ' '.join(context.args)
    if not query:
        update.message.reply_text("Please provide a search query. Example: /search Python")
        return

    search_results = []
    for j in search(query, num_results=5):
        search_results.append(f"<a href=\"{j}\">{j}</a>")

    results = "\n".join(search_results)
    update.message.reply_text(results, parse_mode=ParseMode.HTML)
def main():
    updater = Updater(token=TELEGRAM_API_KEY, use_context=True)
    
    logger.info("Telegram bot started")

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("search", google_search, pass_args=True))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, gpt_answer))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()