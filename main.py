from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


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

    if message_type == 'group' :
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return

    else:
        response: str = handle_response(text)     
    
    print('Bot:', response)

    await update.message.reply_text(response)


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