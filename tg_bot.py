from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from dotenv import load_dotenv
import os

# Open Api Key load
dotenv_path = './.env'
load_dotenv(dotenv_path)
TOKEN: Final = os.getenv('GEBERICH_OPTG_TOKENENAI_API_KEY')


openai.api_key = os.getenv('GEBERICH_OPENAI_API_KEY')
BOT_USERNAME: Final = '@traveltiesbot'

start_message = """
Привет! Hello! ¡Hola! Bonjour! こんにちは! 您好!
Translate, Learn, Communicate!
🗺 Ваш ключ к миру языков и культур. Готовы начать? Напишите текст для перевода!
"""

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(start_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text('Hi! How can I help?')


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text('Hi! Here is a custom command')

