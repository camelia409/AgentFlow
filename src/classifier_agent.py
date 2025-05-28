import json
import os
from utils import extract_pdf_text, detect_intent
from json_agent import JSONAgent
from email_agent import EmailAgent
import logging

logger = logging.getLogger(__name__)

class ClassifierAgent:
    def __init__(self, memory_store):
        self.memory_store = memory_store
        self.json_agent = JSONAgent(self.memory_store)
        self.email_agent = EmailAgent(self.memory_store)

    def classify_and_route(self, input_data, source="unknown"):
        if isinstance(input_data, str) and os.path.exists(input_data):
            if input_data.endswith(".pdf"):
                input_type = "PDF"
                content = extract_pdf_text(input_data)
            elif input_data.endswith(".json"):
                input_type = "JSON"
                with open(input_data, 'r') as f:
                    content = json.load(f)
            else:
                input_type = "Email"
                with open(input_data, 'r', encoding='utf-8') as f:
                    content = f.read()
        else:
            input_type = "Email"
            content = input_data

        intent = detect_intent(content, input_type=input_type)
        logger.info(f"Classified {source} as {input_type} with intent {intent}")

        thread_id = self.memory_store.log(source, input_type, intent, {})

        if input_type == "JSON":
            result = self.json_agent.process(content, intent=intent)
        else:
            result = self.email_agent.process(content, input_type)
            # Ensure EmailAgent intent matches ClassifierAgent intent
            result["data"]["intent"] = intent

        self.memory_store.store[thread_id]["extracted_data"] = result
        return thread_id, result