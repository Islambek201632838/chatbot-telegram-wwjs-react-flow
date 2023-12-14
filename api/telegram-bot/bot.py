from telegram.ext import *
from telegram import Update
import httpx
import logging
from datetime import datetime
from keys import TELEGRAM_TOKEN, API_URL, USER_INTERACTION_URL, CHAT_ID_ADMIN

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def get_json():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(API_URL)
            response.raise_for_status()
            flow_data = response.json()
            response = flow_data.get('response', [])
            return response
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return {}

async def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    schema = await get_json()
    await context.bot.send_message(chat_id=chat_id, text=schema.get("start", "Default start message"))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text
    chat_id = update.effective_chat.id
    schema = await get_json()
    await context.bot.send_message(chat_id=chat_id, text=schema.get("unknown_command", "Default unknown command message"))

async def consultation(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    schema = await get_json()
    await context.bot.send_message(chat_id=chat_id, text=schema.get("consultation", "Default consultation message"))

async def text_call_me(action, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_name = update.effective_user.name
    chat_id = update.effective_chat.id
    schema = await get_json()
    
    try:
        async with httpx.AsyncClient() as client:
            await context.bot.send_message(chat_id=chat_id, text=schema.get("text_call_me","Default action message") )
            info = f"Пользователь ({user_name}) оставил заявку на получение консультации {action}. Дата и время заявки: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}. Необходимо с ним связаться."
            await context.bot.send_message(chat_id=CHAT_ID_ADMIN, text=info)

            post_data = {
                'whatsapp_user_name': f'telegram: {user_name}',
                'phone_number': 'no phone number',
                'action': action,
                'date': datetime.now().date().isoformat(),
                'time': datetime.now().time().isoformat()
            }
            await client.post(USER_INTERACTION_URL, json=post_data)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        await context.bot.send_message(chat_id=chat_id, text='Произошла ошибка.')

async def text_me(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await text_call_me('написать', update, context)

async def call_me(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await text_call_me('позвонить', update, context)

def error(update: Update, context: CallbackContext):
    logging.warning(f'Update "{update}" caused error "{context.error}"')

if __name__ == '__main__':
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('consultation', consultation))
    application.add_handler(CommandHandler('text_me', text_me))
    application.add_handler(CommandHandler('call_me', call_me))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error)

    application.run_polling(1.0)
