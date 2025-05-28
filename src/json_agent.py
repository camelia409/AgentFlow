class JSONAgent:
    def __init__(self, memory_store):
        self.memory_store = memory_store
        self.target_schema = {
            "request_type": str,
            "item": str,
            "quantity": int,
            "company": str
        }

    def process(self, json_data, intent):
        result = {"status": "success", "data": {}, "anomalies": []}
        try:
            for key, expected_type in self.target_schema.items():
                if key in json_data:
                    if isinstance(json_data[key], expected_type):
                        result["data"][key] = json_data[key]
                    else:
                        result["anomalies"].append(f"Invalid type for {key}")
                else:
                    result["anomalies"].append(f"Missing field: {key}")
            result["data"]["intent"] = intent
            if result["anomalies"]:
                result["status"] = "warning"
        except Exception as e:
            result["status"] = "error"
            result["anomalies"].append(str(e))
            result["data"]["intent"] = intent
        return result