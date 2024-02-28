from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv
import csv
from saveResources import create_pages_for_urls

# Define the CSV file path
CSV_FILE_PATH = 'D:/Python Projects/Second-Brain-Bot/resources/urls.csv'

# Load environment variables from .env file
load_dotenv()

# Retrieve the integration token from the environment variable
TOKEN: Final = os.getenv("TELEGRAM_BOT_TOKEN")
BOT_USERNAME: Final = '@A_SecondBrainBot'

#Commands

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hii! Thanks for starting me :), I am your Second Brain!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('For any issues contact my creator Ash! (@AshiHaque)')

async def howto_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Paste the url(s) for the rource(s) that you want to Save :)')        


#Responses

#def handle_response(text: str) -> str:
    #processed = text.lower()  # Convert text to lowercase
    
    #if 'hello' in processed:
        #return 'Hiii!'
    
    #if 'test1' in processed:
        #return 'Oneee'
    
    #if 'test2' in processed:
        #return 'Twooo'
    
   # return 'I do not understand what you wrote :('


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User({update.message.chat.id}) in {message_type}: "{text}"')

    # Extract URL from the message
    urls = extract_urls(text)

    # Check if any URLs were found
    if urls:
        # Append the URLs to the CSV file
        append_urls_to_csv(urls)

        # Call the function to create Notion pages
        create_pages_for_urls(urls)

        # Respond to the user
        response = f"Received {len(urls)} URL(s). Saved to CSV file and Notion."
    else:
        response = "No valid URLs found in the message."

    print('Bot:', response)

    await update.message.reply_text(response)

def extract_urls(text: str) -> list:
    # This is a simple example function to extract URLs from the text
    return [word for word in text.split() if word.startswith("http")]

def append_urls_to_csv(urls: list):
    # Append the URLs to the CSV file
    with open(CSV_FILE_PATH, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(urls)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
     print(f'Update({update}) caused error {context.error}')

if __name__ == '__main__':
    print('Starting bot...')
    app=Application.builder().token(TOKEN).build()


# Commands

app.add_handler(CommandHandler('start', start_command))

app.add_handler(CommandHandler('help', help_command))

app.add_handler(CommandHandler('howto', howto_command))

# Messages

app.add_handler(MessageHandler(filters.TEXT, handle_message))

# Errors

app.add_error_handler(error)

# Polls the bot

print('Polling...')

app.run_polling(poll_interval=3)
