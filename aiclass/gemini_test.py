# # test_gemini.py
# import os
# import google.generativeai as genai
# from dotenv import load_dotenv

# load_dotenv()
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# model = genai.GenerativeModel("gemini-pro")
# chat = model.start_chat(history=[])
# response = chat.send_message("What is Django?")
# print("✅ Gemini says:", response.text)



import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

models = genai.list_models()
for model in models:
    print(model.name, model.supported_generation_methods)
