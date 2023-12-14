from telegram.ext import *
from telegram import Update
import requests
import logging
from datetime import datetime
from keys import TELEGRAM_TOKEN, API_URL, USER_INTERACTION_URL


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text = 'Hi! I am your Telegram bot.')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text = 'help')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text
    chat_id = update.effective_chat.id
    user_name = update.effective_user.name

    try:
        flow_data = requests.get(API_URL).json()
        nodes = flow_data.get('nodes', [])
        
        if nodes:
            if message == nodes[1]['label']:
                await context.bot.send_message(chat_id=chat_id, text=nodes[2]['label'])
                action = 'Request Consultation'
            elif message == nodes[3]['label'] or message == nodes[4]['label']:
                await context.bot.send_message(chat_id=chat_id, text=nodes[5]['label'])
                action = 'Call' if message == nodes[3]['label'] else 'Write'
                # Information to send
                info = f"A person ({user_name}) has requested a consultation: {action}. Date and time of the request: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}. They need to be contacted."
                await context.bot.send_message(chat_id='+77076344538', text=info)

                # Posting user interaction
                post_data = {
                    'whatsapp_user_name': f'telegram: {user_name}',
                    'phone_number': '',
                    'action': action,
                    'date': datetime.now().date().isoformat(),
                    'time': datetime.now().time().isoformat()
                }
                await requests.post(USER_INTERACTION_URL, json=post_data)

    except Exception as e:
        print(f"An error occurred: {e}")

def error(update, context):
    """Log errors caused by updates."""
    logging.warning(f'Update "{update}" caused error "{context.error}"')

if __name__ == '__main__':
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Commands
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    # Run bot
    application.run_polling(1.0)
    application.add_error_handler(error)

