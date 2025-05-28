import pdfplumber
from transformers import pipeline
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Global classifier
_classifier = None

def initialize_classifier():
    global _classifier
    if _classifier is None:
        try:
            cache_dir = "./model_cache"
            os.makedirs(cache_dir, exist_ok=True)
            logger.info("Initializing classifier: typeform/distilbert-base-uncased-mnli")
            _classifier = pipeline(
                "zero-shot-classification",
                model="typeform/distilbert-base-uncased-mnli",
                cache_dir=cache_dir
            )
        except Exception as e:
            logger.error(f"Failed to initialize classifier: {str(e)}")
            _classifier = None

def extract_pdf_text(file_path):
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            return text.strip() if text else "No text extracted from PDF"
    except Exception as e:
        logger.error(f"PDF extraction error: {str(e)}")
        return f"Error reading PDF: {str(e)}"

def detect_intent(text, input_type="Unknown"):
    # Ensure text is a string
    text = str(text)
    # Rule-based for emails to ensure reliability
    if input_type == "Email":
        text_lower = text.lower()
        logger.info(f"Email text for intent detection: {text_lower[:100]}...")
        if any(keyword in text_lower for keyword in ["complaint", "defective", "issue", "problem", "faulty"]):
            logger.info(f"Rule-based intent: Complaint for text: {text[:100]}...")
            return "Complaint"
        elif any(keyword in text_lower for keyword in ["rfq", "quote", "request for quote"]):
            logger.info(f"Rule-based intent: Request for Quote (RFQ) for text: {text[:100]}...")
            return "Request for Quote (RFQ)"
        elif any(keyword in text_lower for keyword in ["invoice", "amount", "payment", "bill"]):
            logger.info(f"Rule-based intent: Invoice for text: {text[:100]}...")
            return "Invoice"
        elif any(keyword in text_lower for keyword in ["regulation", "compliance"]):
            logger.info(f"Rule-based intent: Regulation for text: {text[:100]}...")
            return "Regulation"
        logger.warning(f"Rule-based intent: Unknown for text: {text[:100]}...")
        return "Unknown"

    # Initialize classifier if not already done
    initialize_classifier()
    
    try:
        if _classifier is not None:
            candidate_labels = ["Invoice", "Request for Quote (RFQ)", "Complaint", "Regulation"]
            result = _classifier(
                text[:512],
                candidate_labels,
                multi_label=False,
                hypothesis_template="This text is related to a {} document or issue."
            )
            intent = result["labels"][0]
            scores = {label: round(score, 3) for label, score in zip(result["labels"], result["scores"])}
            logger.info(f"LLM intent: {intent}, scores: {scores} for text: {text[:100]}...")
            return intent
        else:
            raise Exception("Classifier not initialized")
    except Exception as e:
        logger.error(f"LLM intent detection failed: {str(e)}")
        text_lower = text.lower()
        if any(keyword in text_lower for keyword in ["invoice", "amount", "payment", "bill"]):
            logger.warning("Using fallback: Invoice")
            return "Invoice"
        elif any(keyword in text_lower for keyword in ["rfq", "quote", "request for quote"]):
            logger.warning("Using fallback: Request for Quote (RFQ)")
            return "Request for Quote (RFQ)"
        elif any(keyword in text_lower for keyword in ["complaint", "defective", "issue", "problem", "faulty"]):
            logger.warning("Using fallback: Complaint")
            return "Complaint"
        elif any(keyword in text_lower for keyword in ["regulation", "compliance"]):
            logger.warning("Using fallback: Regulation")
            return "Regulation"
        logger.warning(f"Fallback intent: Unknown for text: {text[:100]}...")
        return "Unknown"