# Multi-Agent AI System

This project implements a multi-agent AI system that processes inputs in PDF, JSON, or Email format, classifies their intent using `typeform/distilbert-base-uncased-mnli` (with rule-based fallback for emails and other formats if LLM fails), and routes them to specialized agents. A shared memory module ensures traceability, and a Streamlit web interface provides a dynamic demo with intent distribution visualization.

---

## ⚙️ Setup

### 1. Clone the Repository:
```bash
git clone <repo-url>
cd multi_agent_system
```

### 2. Set Up Virtual Environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies:
```bash
pip install -r requirements.txt
```

### 4. Download LLM Model:
```bash
python src/download_model.py
```
This caches the DistilBERT model locally.

### 5. Create Sample PDF:
```bash
python src/create_sample_pdf.py
```

---

## 🚀 Run the System

### 🔹 Command Line:
```bash
python src/main.py
```
Processes sample files and saves logs to `outputs/logs.json`.

### 🔹 Web Interface:
```bash
streamlit run src/app.py
```
Open [http://localhost:8501](http://localhost:8501) to upload files, view results, and see the intent distribution chart.

---

## 🎥 Demo

A video demo is available in `vid/demo.mp4`, showing the system processing inputs via the Streamlit interface with an intent distribution chart.

---

## 📁 Folder Structure

```
multi_agent_system/
├── README.md
├── requirements.txt
├── src/
│   ├── main.py
│   ├── classifier_agent.py
│   ├── json_agent.py
│   ├── email_agent.py
│   ├── memory_store.py
│   ├── utils.py
│   ├── app.py                
│   ├── create_sample_pdf.py  
│   └── download_model.py     
├── inputs/
│   ├── sample.pdf
│   ├── sample.json
│   └── sample_email.txt
├── outputs/
│   ├── logs.json
│   └── screenshots/
├── model_cache/              
└── vid/
    └── demo.mp4
```
