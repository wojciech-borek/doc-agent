import openai
import pdfplumber
from googletrans import Translator

from fuzzywuzzy import fuzz

openai.api_key = ""

translator = Translator()

def detect_language(text):
    return translator.detect(text).lang

def translate_text(text, target_language):
    return translator.translate(text, dest=target_language).text

def load_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text

def chat_with_openai(query, pdf_text):
    user_language = detect_language(query)

    if user_language != "pl":
        translated_query = translate_text(query, "pl")
    else:
        translated_query = query

    response = ask_openai(query, pdf_text)

    if user_language != "pl":
        response = translate_text(response, user_language)
    
    return response

def ask_openai(question, context):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that only answers based on the provided documentation."},
            {"role": "user", "content": f"Dokumentacja: {context}\nPytanie: {question}\nOdpowiedź:"}
        ],
        max_tokens=300,
        temperature=0.7,
    )
    return response.choices[0].message['content'].strip()

def main():
    pdf_text = load_text_from_pdf("api.pdf")
    
    while True:
        user_question = input("Ask a question (or type 'exit', to end): ")
        if user_question.lower() == "exit":
            print("Thank you for using the FAQ Chatbot!")
            break
        
        response = chat_with_openai(user_question, pdf_text)
        print(f"Answer: {response}")

if __name__ == "__main__":
    main()