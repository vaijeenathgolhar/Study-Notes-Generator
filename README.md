# Smart Study Notes Generator 📚🤖

An AI-powered study assistant that generates **summaries, key points, and quiz questions** from any topic using **LangGraph workflows and LLMs**.

This project demonstrates how **AI pipelines can automate learning workflows** for students.

---

## 🚀 Live Demo

Try the application here:

🔗 https://study-notes-generator-kwjpmchsgngrhe2ekl93pm.streamlit.app/

---

## Features

* AI-generated **topic summaries**
* **Bullet-point study notes**
* **Auto-generated quiz questions with answers**
* Built using **LangGraph workflow pipelines**
* Interactive **Streamlit web interface**

---

## Architecture

The application uses a **LangGraph workflow pipeline**.

Topic Input
↓
Summary Generation
↓
Key Points Extraction
↓
Quiz Generation

This pipeline is implemented using **LangGraph nodes and edges**.

---

## Tech Stack

* Python
* LangGraph
* LangChain
* Groq LLM
* Streamlit
* Prompt Engineering

---

## Project Structure

```
Study-Notes-Generator-AI
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── utils/
```

---

## Installation

Clone the repository:

```
git clone https://github.com/vaijeenathgolhar/Study-Notes-Generator-AI.git
cd Study-Notes-Generator-AI
```

Install dependencies:

```
pip install -r requirements.txt
```

---

## Setup Environment Variables

Create a `.env` file and add your Groq API key:

```
GROQ_API_KEY=your_api_key_here
```

---

## Run the Application

Start the Streamlit app:

```
streamlit run app.py
```

The app will open in your browser.

---

## Example Usage

Enter a topic such as:

```
Transformer Architecture
```

The AI will generate:

* Summary
* Key study points
* Quiz questions

---

## Future Improvements

* PDF document study notes generation
* Export notes as PDF
* Flashcard generation
* RAG-based knowledge retrieval

---

## Author

**Vaijeenath Golhar**

AI / ML Engineer | Generative AI Developer
