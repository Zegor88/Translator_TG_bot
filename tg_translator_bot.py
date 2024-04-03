from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import openai
from openai import OpenAI
import os

# Load environment variables
dotenv_path = './.env'
load_dotenv(dotenv_path)
TOKEN = os.getenv('TG_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

# Global dictionary to store user language preferences
user_languages = {}

# Language options for the bot
language_options = {
    'Русский (Rus)': 'Russian (Rus)',
    'Srpski (latinica)': 'Serbian (Latin)',
    'Српски (ћирилица)': 'Serbian (Cyrillic)',
    'English (USA)': 'English',
    'Türk': 'Turkish'
}

# Start message
start_message = """
Привет! Hello! ¡Hola! Bonjour! こんにちは! 您好!
"""

client = OpenAI()
# Function for OpenAI response
def gpt_response(system_message, prompt_text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0,
        max_tokens=100
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt_text}
        ]
    )   
    return response.choices[0].message.content

# Command Handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(start_message)

async def language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton(lang)] for lang in language_options.keys()]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text('Hi! Select the language', reply_markup=reply_markup)

# Handle incoming messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    # Инициализируем output_language значением по умолчанию
    output_language = 'Russian (RUS)'  # Значение по умолчанию, на случай, если язык не был выбран

    if text in language_options:
        # Обновляем языковые предпочтения пользователя
        user_languages[user_id] = language_options[text]
        await update.message.reply_text(f"Language set to {text}. Please enter text to translate.")
        return
    elif user_id in user_languages:
        # Используем выбранный язык пользователя для перевода
        output_language = user_languages.get(user_id)

    # Определяем язык входящего текста
    input_language_prompt = "Please identify the language of the user's text. Respond only with the language name. No more words."
    input_language = gpt_response(input_language_prompt, text)

    # Переводим текст
    translation_prompt = f"""
    Please translate the following text from {input_language} language to {output_language} language, ensuring to maintain the accuracy and nuances of the original. 
    Consider the context and cultural aspects to make the translation as natural and precise as possible. 
    Avoid literal translation, while accurately conveying the meaning of each sentence and phrase. 
    Be sure, your response is absolutely in {output_language}.
    The prompt should take into account the specific nature of the text, whether it be a technical document, literary work, business correspondence, or informal conversation.
    """
    translated_text = gpt_response(translation_prompt, text)
    await update.message.reply_text(translated_text)



# Error handling
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} causes error {context.error}')

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('language', language))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Register error handler
    app.add_error_handler(error)

    print('Bot is polling...')
    app.run_polling()