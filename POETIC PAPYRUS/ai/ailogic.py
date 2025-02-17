import os
from dotenv import load_dotenv
import google.generativeai as genai
import fitz  

load_dotenv()

api_key = os.getenv("AI_API_KEY")

genai.configure(api_key=api_key)

def extract_text_from_pdf(pdf_path):
    try:

        # Open the PDF file and Extract
        document = fitz.open(pdf_path)
        text = ""
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            text += page.get_text()
        
        return text  
    
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

def process_input_with_pdf(pdf_file_path):
    pdf_text = extract_text_from_pdf(pdf_file_path)
    if pdf_text:

    #genai configuration
        generation_config = {
            "temperature": 0.95,
            "top_p": 1,
            "top_k": 0,
            "max_output_tokens": 2048,
        }
        
        model = genai.GenerativeModel(
            model_name="gemini-1.0-pro",
            generation_config=generation_config,
        )
    #prompt 

        additional_phrases = ", make it into a poem for kids include everything"
        message_to_send = pdf_text + "\n\n" + additional_phrases
        
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(message_to_send)
        
        return response.text
    else:
        return "Failed to extract text from the PDF."
