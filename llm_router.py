import os
from dotenv import load_dotenv
from anthropic import Anthropic
from openai import OpenAI
import google.generativeai as genai

load_dotenv()

def get_llm_response(prompt: str, provider: str = 'anthropic', model: str = None) -> str:
    if provider == 'anthropic':
        model = model or 'claude-haiku-4-5-20251001'
        client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        response = client.messages.create(
            model=model, max_tokens=1500,
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response.content[0].text
    elif provider == 'openai':
        model = model or 'gpt-4o-mini'
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model=model,
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response.choices[0].message.content
    elif provider == 'gemini':
        model = model or 'gemini-1.5-flash'
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        model_obj = genai.GenerativeModel(model)
        response = model_obj.generate_content(prompt)
        return response.text
    else:
        raise ValueError(f'Unknown provider: {provider}')
