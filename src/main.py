import json
from classifier_agent import ClassifierAgent
from memory_store import MemoryStore

def main():
    memory_store = MemoryStore()
    classifier = ClassifierAgent(memory_store)

    # Test inputs
    inputs = [
        "inputs/sample.pdf",
        "inputs/sample.json",
        "inputs/sample_email.txt"
    ]

    # Process each input
    for input_path in inputs:
        print(f"\nProcessing {input_path}...")
        thread_id, result = classifier.classify_and_route(input_path, source=input_path)
        print(f"Thread ID: {thread_id}")
        print(f"Result: {json.dumps(result, indent=2)}")
        print(f"Memory: {json.dumps(memory_store.get(thread_id), indent=2)}")

    # Save logs
    with open("outputs/logs.json", "w") as f:
        json.dump(memory_store.store, f, indent=2)

if __name__ == "__main__":
    main()