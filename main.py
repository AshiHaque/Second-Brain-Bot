from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import csv

# Define the CSV file path
CSV_FILE_PATH = 'D:/Python Projects/Second-Brain-Bot/resources/urls.csv'


TOKEN: Final = '7004294087:AAFyTdzctBZ-MWyspCXD0O21HDQTFAvYd9g'
BOT_USERNAME: Final = '@A_SecondBrainBot'

#Commands

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hii! Tanks for starting me, I am your Second Brain')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Help')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Custom')        


#Responses

def handle_response(text: str) -> str:
    processed = text.lower()  # Convert text to lowercase
    
    if 'hello' in processed:
        return 'Hiii!'
    
    if 'test1' in processed:
        return 'Oneee'
    
    if 'test2' in processed:
        return 'Twooo'
    
    return 'I do not understand what you wrote :('


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

        # Respond to the user
        response = f"Received {len(urls)} URL(s). Saved to CSV file."
    else:
        response = "No valid URLs found in the message."

    print('Bot:', response)

    await update.message.reply_text(response)

def extract_urls(text: str) -> list:
    # This is a simple example function to extract URLs from the text
    # You may want to use a more robust method for real-world use cases
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

app.add_handler(CommandHandler('custom', custom_command))

# Messages

app.add_handler(MessageHandler(filters.TEXT, handle_message))

# Errors

app.add_error_handler(error)

# Polls the bot

print('Polling...')

app.run_polling(poll_interval=3)
