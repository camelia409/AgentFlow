import re
from utils import detect_intent
import logging

logger = logging.getLogger(__name__)

class EmailAgent:
    def __init__(self, memory_store):
        self.memory_store = memory_store

    def process(self, content, input_type):
        result = {"status": "success", "data": {}, "anomalies": []}
        try:
            # Read content if it's a file path
            if input_type == "Email" and isinstance(content, str) and content.endswith(".txt"):
                with open(content, 'r', encoding='utf-8') as f:
                    content = f.read()

            # Extract fields using regex
            sender_match = re.search(r"From: ([^\n]+)", content, re.IGNORECASE)
            subject_match = re.search(r"Subject: ([^\n]+)", content, re.IGNORECASE)
            body_match = re.search(r"(?:Subject: [^\n]+\n\n)([\s\S]+)", content, re.IGNORECASE)

            result["data"]["sender"] = sender_match.group(1).strip() if sender_match else "Unknown"
            result["data"]["subject"] = subject_match.group(1).strip() if subject_match else "Unknown"
            result["data"]["body"] = body_match.group(1).strip() if body_match else content
            result["data"]["urgency"] = "High" if any(keyword in content.lower() for keyword in ["urgent", "asap"]) else "Normal"
            
            # Use detect_intent for consistency
            result["data"]["intent"] = detect_intent(result["data"]["body"], input_type=input_type)
            logger.info(f"EmailAgent intent set to: {result['data']['intent']}")
        except Exception as e:
            result["status"] = "error"
            result["anomalies"].append(str(e))
            result["data"]["intent"] = "Unknown"
            logger.error(f"Email processing error: {str(e)}")
        return result