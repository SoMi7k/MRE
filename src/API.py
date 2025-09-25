from openai import OpenAI
import streamlit as st
from abc import ABC, abstractmethod
import features.env as ft
from anthropic import Anthropic
import src.data as data
import requests
from transformers import AutoTokenizer, AutoModelForTokenClassification, AutoModelForCausalLM
from transformers import pipeline

class Extractor(ABC):
    """
    Abstract class for every LLM extractor in this program.

    Attributes:
        text: Text for extraction.
        prompt: Information for AI model what it should do.
        json: Output required JSON structure.
    """
    def __init__(self, data: data.InputData, api_key: ft.API_keys):
        """Inits Extractor parametrs"""
        self.data = data
        self.api_key = api_key
        self.result = None

    @abstractmethod
    def generate(self) -> None:
        """There will be logic of any AI model API."""
        pass

    @abstractmethod
    def printer(self):
        if self.result:
            return st.markdown("*" + self.result + "*")
        else:
            return st.markdown("Result is empty.\n" \
            "- Check if function generate was launched.\n" \
            "- Check class attributes if they're not damaged/empty.")

class openAI(Extractor):
    """
    OpenAI API class.
    
    Attributes:
        Extractor: Instance of abstract class Exctractor
    """
    def __init__(self, data, api_key):
        super().__init__(data, api_key)
        
        
    def generate(self):
        """Calls OpenaAI client."""
        client = OpenAI(api_key=self.api_key.get_api_key())

        if self.data.text is None or self.data.prompt is None or self.data.json is None:
            return None
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": self.data.prompt},
                {"role": "user", "content": self.data.text}
            ]
        )

        self.result = response.choices[0].message.content

        """
        response = client.responses.parse(
            model="gpt-4o-2024-08-06",
            input=[
                {"role": "system", "content": self.data.prompt},
                {
                    "role": "user",
                    "content": self.data.text,
                },
            ],
            text_format=self.data.json,
        )
        
        self.result = response.output_parsed
        """

    def printer(self):
        return super().printer()
        
class Claude(Extractor):
    """
    Claude Sonnet API class.
    
    Attributes:
        Extractor: Instance of abstract class Exctractor
    """
    def __init__(self, data, api_key):
        super().__init__(data, api_key)

    def generate(self):
        client = Anthropic(api_key=self.api_key.get_api_key())

        if self.data.text is None or self.data.prompt is None or self.data.json is None:
            return None

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": "Hello, world"}
            ]
        )

        print(response.content[0].text)
    
    def printer(self):
        return super().printer()

class Mistral(Extractor):
    """
    Claude Sonnet API class.
    
    Attributes:
        Extractor: Instance of abstract class Exctractor
    """
    def __init__(self, data, api_key):
        super().__init__(data, api_key)

    def generate(self):
        if self.data.text is None or self.data.prompt is None or self.data.json is None:
            return None

        headers = {
            "Authorization": f"Bearer {self.api_key.get_api_key()}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8501/"
        }

        payload = {
            "model": "mistral-7b",  # Nebo "mixtral-8x7b-32768"
            "messages": [
                {"role": "user", "content": self.data.text}
            ],
            "max_tokens": 1024
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )

        if response.status_code != 200:
            raise Exception(f"API request failed: {response.status_code} - {response.text}")

        data = response.json()
        print(data["choices"][0]["message"]["content"])
        return data["choices"][0]["message"]["content"]
    
    def printer(self):
        return super().printer()

"""
class Gemini(Extractor):
    
    Gemmini API class.
    
    Attributes:
        Extractor: Instance of abstract class Exctractor
    
    def __init__(self, data, api_key):
        super().__init__(data, api_key)

    def generate(self):
        # Kontrola, zda jsou všechna potřebná data k dispozici
        if self.data.text is None or self.data.prompt is None or self.data.json is None:
            # Měli byste zvážit vyvolání výjimky nebo vrácení chybového stavu místo None
            print("Chyba: Chybí vstupní data (text, prompt nebo JSON schéma).")
            return None

        client = genai.Client(api_key=self.api_key.get_api_key())

        # 1. Nahrání souboru (předpokládáme, že self.data.text je filepath)
        try:
            uploaded_file = client.files.upload(file=self.data.text)
        except Exception as e:
            print(f"Chyba při nahrávání souboru {self.data.text}: {e}")
            return None

        # 2. Příprava obsahu pro model
        contents = [
            types.Content(
                role="user",
                parts=[
                    # Připojení nahraného obrázku
                    types.Part.from_uri(
                        file_uri=uploaded_file.uri,
                        mime_type=uploaded_file.mime_type,
                    ),
                    # Připojení promptu
                    types.Part.from_text(text=self.data.prompt)
                ],
            )
        ]

        # 3. Konfigurace modelu pro structured output s JSON schématem
        # Použijeme model "gemini-1.5-flash" jak je v původním kódu
        # response_json_schema se očekává jako Python dictionary, ne cesta k souboru
        config = types.GenerateContentConfig(
            response_mime_type='application/json',
            response_json_schema=self.data.json # Předpokládá se, že self.data.json je již načtený dict
        )

        try:
            # Přímé volání generate_content bez streamování pro structured output
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=contents,
                config=config,
            )
            
            # Po dokončení volání, zkontrolovat, zda response obsahuje text
            # Model s 'response_mime_type': 'application/json' by měl vrátit validní JSON řetězec v response.text
            if response.text:
                # Parsujeme JSON řetězec do Python slovníku
                self.result = json.loads(response.text)
                return self.result
            else:
                print("Model nevrátil žádný text (JSON).")
                return None

        except Exception as e:
            print(f"Došlo k chybě při generování obsahu: {e}")
            return None

    
    def printer(self):
        if self.result:
            return st.markdown("*" + self.result + "*")
        else:
            return st.markdown("Result is empty.\n" \
            "- Check if function generate was launched.\n" \
            "- Check class attributes if they're not damaged/empty.")
"""

class ClinicalBERT(Extractor):
    """
    ClinicalBERT Extractor using Hugging Face pipeline (NER).
    """
    def __init__(self, data, model_name="emilyalsentzer/Bio_ClinicalBERT", task="ner", device=-1):
        super().__init__(data, None)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForTokenClassification.from_pretrained(model_name)
        self.pipeline = pipeline(task=task, model=self.model, tokenizer=self.tokenizer, device=device)

    def generate(self):
        if self.data.text is None:
            return None
        
        entities = self.pipeline(self.data.text)
        self.result = entities

    def printer(self):
        return super().printer()

class BioGPT(Extractor):
    """
    BioGPT Extractor using Hugging Face transformers.
    """
    def __init__(self, data, model_name="microsoft/biogpt", device="cpu"):
        super().__init__(data, None)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
        self.device = device

    def generate(self):
        if self.data.text is None:
            return None
        
        input_ids = self.tokenizer.encode(self.data.text, return_tensors="pt").to(self.device)
        output = self.model.generate(input_ids, max_length=256)
        decoded = self.tokenizer.decode(output[0], skip_special_tokens=True)
        self.result = decoded
    
    def printer(self):
        return super().printer()

    
class Generator():
    def __init__(self, model: Extractor|None):
        self.__model = model

    def set_new_model(self, model: Extractor):
        self.__model = model
    
    def get_model(self) -> Extractor:
        if self.__model is None:
            raise ValueError("Model is not set. Please set a model before calling get_model().")
        return self.__model