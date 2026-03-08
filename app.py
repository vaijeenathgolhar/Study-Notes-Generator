import streamlit as st

# MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="Smart Study Notes Generator",
    layout="wide"
)

import os
from dotenv import load_dotenv
from typing import TypedDict

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END

import graphviz
from fpdf import FPDF


# -----------------------------
# 1. Load Environment Variables
# -----------------------------
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("GROQ_API_KEY not found. Check your .env file.")
    st.stop()


# -----------------------------
# 2. Initialize LLM
# -----------------------------
@st.cache_resource
def load_llm():
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.4,
        groq_api_key=groq_api_key
    )

llm = load_llm()


# -----------------------------
# 3. Graph State
# -----------------------------
class StudyState(TypedDict):
    topic: str
    summary: str
    key_points: str
    quiz: str


# -----------------------------
# 4. Nodes
# -----------------------------
def summarize_node(state: StudyState):

    prompt = ChatPromptTemplate.from_template(
        """
        Summarize the following topic in simple language for students:

        {topic}
        """
    )

    chain = prompt | llm
    result = chain.invoke({"topic": state["topic"]})

    return {"summary": result.content}


def keypoints_node(state: StudyState):

    prompt = ChatPromptTemplate.from_template(
        """
        Convert this summary into clear bullet-point study notes:

        {summary}
        """
    )

    chain = prompt | llm
    result = chain.invoke({"summary": state["summary"]})

    return {"key_points": result.content}


def quiz_node(state: StudyState):

    prompt = ChatPromptTemplate.from_template(
        """
        Create 5 quiz questions with answers from these notes:

        {key_points}
        """
    )

    chain = prompt | llm
    result = chain.invoke({"key_points": state["key_points"]})

    return {"quiz": result.content}


# -----------------------------
# 5. Build Graph
# -----------------------------
@st.cache_resource
def build_graph():

    builder = StateGraph(StudyState)

    builder.add_node("summarizer", summarize_node)
    builder.add_node("keypoints", keypoints_node)
    builder.add_node("quiz_generator", quiz_node)

    builder.set_entry_point("summarizer")

    builder.add_edge("summarizer", "keypoints")
    builder.add_edge("keypoints", "quiz_generator")
    builder.add_edge("quiz_generator", END)

    return builder.compile()


graph = build_graph()


# -----------------------------
# 6. PDF Generator
# -----------------------------
def create_pdf(summary, keypoints, quiz):

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, "AI Study Notes", ln=True)

    pdf.multi_cell(0, 8, "SUMMARY\n" + summary)
    pdf.multi_cell(0, 8, "\nKEY POINTS\n" + keypoints)
    pdf.multi_cell(0, 8, "\nQUIZ\n" + quiz)

    pdf.output("study_notes.pdf")


# -----------------------------
# 7. UI
# -----------------------------
st.title("Smart Study Notes Generator")

st.write("Enter a topic or paste study material and generate notes + quiz.")


topic = st.text_area(
    "Enter Topic",
    height=200
)

result = None

if st.button("Generate"):

    if topic.strip() == "":
        st.warning("Please enter a topic.")

    else:

        with st.spinner("AI is generating notes..."):

            result = graph.invoke({"topic": topic})

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Summary")
            st.write(result["summary"])

            st.subheader("Key Points")
            st.write(result["key_points"])

        with col2:

            st.subheader("Quiz")
            st.write(result["quiz"])

        # PDF Download
        create_pdf(
            result["summary"],
            result["key_points"],
            result["quiz"]
        )

        with open("study_notes.pdf", "rb") as file:

            st.download_button(
                label="Download Notes as PDF",
                data=file,
                file_name="study_notes.pdf",
                mime="application/pdf"
            )


# -----------------------------
# 8. AI Study Assistant
# -----------------------------
if result:

    st.subheader("Ask AI about this topic")

    question = st.text_input("Ask a question")

    if question:

        prompt = f"""
        Topic: {topic}

        Study Notes:
        {result["key_points"]}

        Answer the student's question clearly.

        Question:
        {question}
        """

        response = llm.invoke(prompt)

        st.write(response.content)


# -----------------------------
# 9. LangGraph Workflow
# -----------------------------
st.subheader("LangGraph Workflow")

flow = graphviz.Digraph()

flow.edge("User Input", "Summarizer")
flow.edge("Summarizer", "Key Points")
flow.edge("Key Points", "Quiz Generator")

st.graphviz_chart(flow)