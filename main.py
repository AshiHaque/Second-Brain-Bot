from typing import Final
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv
import re
from saveContent import create_pages_for_url
from scrapeContent import scrape_open_graph_metadata

# Load environment variables from .env file
load_dotenv()

# Retrieve the integration token from the environment variable
TOKEN: Final = os.getenv("TELEGRAM_BOT_TOKEN")
BOT_USERNAME: Final = '@A_SecondBrainBot'

# Commands

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hii! Thanks for starting me :), I am your Second Brain!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('For any issues contact my creator Ash! (@AshiHaque)')

async def howto_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Paste the url(s) for the resource(s) that you want to Save :)')        

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User({update.message.chat.id}) in {message_type}: "{text}"')

    # Extract URL from the message
    urls = extract_url(text)

    # Check if any URLs were found
    if urls:
        # Scrape metadata for each URL asynchronously
        scraped_metadata = []
        for url in urls:
            metadata = await scrape_open_graph_metadata(url)
            scraped_metadata.append(metadata)

        # Call the function to create Notion pages with the scraped content
        await create_pages_for_url(scraped_metadata, urls)

        # Respond to the user
        response = f"Received {len(urls)} URL(s). Scraped metadata and created Notion pages."
    else:
        response = "No valid URLs found in the message."

    print('Bot:', response)

    await update.message.reply_text(response)

def extract_url(text: str) -> list:
    # Regular expression pattern to match URLs
    url_pattern = r'https?://\S+'
    # Extract URLs using regex
    return re.findall(url_pattern, text)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update({update}) caused error {context.error}')

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('howto', howto_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Set the HTTPS webhook URL
    webhook_url = "https://second-brain-bot.onrender.com"
    bot = Bot(TOKEN)
    bot.set_webhook(url=webhook_url)

    # Start the application
    app.run_polling(port=int(os.environ.get("PORT", 8080)))