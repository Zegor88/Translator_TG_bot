import openai
from openai import OpenAI
from dotenv import load_dotenv
import os

# Open Api Key load
dotenv_path = './.env'
load_dotenv(dotenv_path)
openai.api_key = os.getenv('GEBERICH_OPENAI_API_KEY')

client = OpenAI()

# Function for OpenAI response
def gpt_response(system_message, prompt_text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt_text}
        ]
    )
    return response.choices[0].message.content

# Prompt for language extraction
system_message_return_language = f"""
Please identify the language of the user's text. Response only The language name. No more words.
"""

#User Message
user_message = f"""
Dobro jutro! Jaksa poziva drugare na proslavu svog 8.rodjendana 🙂!
"""

input_language = gpt_response(system_message_return_language, user_message)
otput_language = 'Russian'

translation_prompt = f"""
Please translate the following text from {input_language} language to {otput_language} language, ensuring to maintain the accuracy and nuances of the original. 
Consider the context and cultural aspects to make the translation as natural and precise as possible. 
Avoid literal translation, while accurately conveying the meaning of each sentence and phrase. 
The prompt should take into account the specific nature of the text, whether it be a technical document, literary work, business correspondence, or informal conversation.
"""

output_text = gpt_response(translation_prompt, user_message)

print(output_text)