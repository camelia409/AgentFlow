import streamlit as st
import json
import os
from classifier_agent import ClassifierAgent
from memory_store import MemoryStore
import pandas as pd

st.set_page_config(page_title="Multi-Agent AI System", layout="wide", page_icon="🤖")

def main():
    st.markdown(
        """
        <style>
        .main { background-color: #f0f2f6; }
        .stButton>button { background-color: #1f77b4; color: white; }
        .stFileUploader { border: 2px dashed #1f77b4; }
        h1 { color: #1f77b4; }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.title("Multi-Agent AI System")
    st.markdown("Upload a PDF, JSON, or Email (text) file to process it through the AI system.")

    if "memory_store" not in st.session_state:
        st.session_state.memory_store = MemoryStore()
        st.session_state.classifier = ClassifierAgent(st.session_state.memory_store)
        st.session_state.processed_files = set()

    # Reset button to clear processed files
    if st.button("Reset Processed Files"):
        st.session_state.processed_files = set()
        st.success("Processed files reset!")

    st.subheader("Upload File")
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "json", "txt"])
    if uploaded_file is not None:
        file_key = f"{uploaded_file.name}_{uploaded_file.size}"
        if file_key not in st.session_state.processed_files:
            file_path = f"inputs/uploaded_{uploaded_file.name}"
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            with st.spinner("Processing..."):
                thread_id, result = st.session_state.classifier.classify_and_route(file_path, source=uploaded_file.name)
                st.session_state.processed_files.add(file_key)
                st.success("Processing complete!")

            st.subheader("Processing Results")
            st.json(result)
            if result["data"].get("intent", "Unknown") == "Unknown":
                st.warning("Intent classification failed. Check input content or try another file.")

            os.remove(file_path)
        else:
            st.info("File already processed.")

    st.subheader("Shared Memory Logs")
    memory_data = st.session_state.memory_store.store
    if memory_data:
        df = pd.DataFrame([
            {**v, "thread_id": k}
            for k, v in memory_data.items()
        ])
        st.table(df)

        st.subheader("Intent Distribution")
        intent_counts = df["intent"].value_counts().to_dict()
        chart_data = {
            "type": "bar",
            "data": {
                "labels": list(intent_counts.keys()),
                "datasets": [{
                    "label": "Intent Counts",
                    "data": list(intent_counts.values()),
                    "backgroundColor": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"],
                    "borderColor": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"],
                    "borderWidth": 1
                }]
            },
            "options": {
                "scales": {
                    "y": {
                        "beginAtZero": True,
                        "title": {"display": True, "text": "Count"}
                    },
                    "x": {
                        "title": {"display": True, "text": "Intent"}
                    }
                }
            }
        }
        st.markdown("### Intent Distribution Chart")
        st.components.v1.html(f"""
            <div style='width: 100%; height: 400px;'>
                <canvas id='intentChart'></canvas>
                <script src='https://cdn.jsdelivr.net/npm/chart.js'></script>
                <script>
                    const ctx = document.getElementById('intentChart').getContext('2d');
                    new Chart(ctx, {json.dumps(chart_data)});
                </script>
            </div>
        """, height=400)

    st.subheader("Test with Sample Files")
    if st.button("Process Sample Files"):
        sample_files = ["inputs/sample.pdf", "inputs/sample.json", "inputs/sample_email.txt"]
        for file_path in sample_files:
            if os.path.exists(file_path):
                file_key = f"{file_path}_{os.path.getsize(file_path)}"
                if file_key not in st.session_state.processed_files:
                    st.write(f"Processing {file_path}...")
                    thread_id, result = st.session_state.classify_and_route(file_path, source=file_path)
                    st.session_state.processed_files.add(file_key)
                    st.json(result)
                    if result["data"].get("intent", "Unknown") == "Unknown":
                        st.warning(f"Intent classification failed for {file_path}. Check input content.")
                else:
                    st.info(f"{file_path} already processed.")
            else:
                st.error(f"Sample file {file_path} not found.")

    with open("outputs/logs.json", "w") as f:
        json.dump(st.session_state.memory_store.store, f, indent=2)

if __name__ == "__main__":
    main()