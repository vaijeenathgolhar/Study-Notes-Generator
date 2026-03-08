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
# 6. UI
# -----------------------------
st.title("Smart Study Notes Generator")

st.write("Enter a topic or paste study material and generate notes + quiz.")


topic = st.text_area(
    "Enter Topic",
    height=200
)

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

            