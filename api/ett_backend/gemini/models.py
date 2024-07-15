import os
from .utils import read_ai_prompt
import google.generativeai as genai

class GeminiModel:

    def __init__(self):
        self._api_key = os.getenv("GOOGLE_API_KEY")
        if not self._api_key:
            raise Exception("Google API key is not set.")
        genai.configure(api_key=self._api_key)

        self._prompt_file_path = os.path.join(os.path.dirname(__file__), 'gemini_prompt.txt')
        if not self._prompt_file_path:
            raise Exception("Cannot find gemini_prompt.txt")

        self._system_instructions = read_ai_prompt(self._prompt_file_path)
        if not self._system_instructions:
            raise Exception("Cannot read gemini_prompt.txt")

    def set_model(self):
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash-latest',
            generation_config=genai.GenerationConfig(
                candidate_count=1,
                temperature=1.25,
                response_mime_type='application/json',
            ),
            system_instruction=self._system_instructions,
        )

        return model

