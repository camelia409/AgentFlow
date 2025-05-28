import uuid
import time

class MemoryStore:
    def __init__(self):
        self.store = {}

    def log(self, source, input_type, intent, extracted_data):
        thread_id = str(uuid.uuid4())
        self.store[thread_id] = {
            "source": source,
            "type": input_type,
            "intent": intent,
            "timestamp": time.time(),
            "extracted_data": extracted_data
        }
        return thread_id

    def get(self, thread_id):
        return self.store.get(thread_id, {})