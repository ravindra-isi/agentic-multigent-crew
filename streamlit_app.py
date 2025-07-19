# streamlit.py
import streamlit as st
from dotenv import load_dotenv
from crewai import Crew, Process
from agents_config import document_agent, query_agent, research_agent, manager_agent
from agent_task import manager_decision_task
from pypdf import PdfReader
import tempfile
import json



# Load .env environment variables
load_dotenv()

st.set_page_config(page_title="AI Agent Crew", layout="centered")
st.title("📄 Intelligent Document & Query Assistant")

# User Inputs
uploaded_file = st.file_uploader("Upload a PDF Document (Optional):", type="pdf")
user_query = st.text_input("Enter your question:", placeholder="What is the summary of this PDF?")

# Helper: Extract text from uploaded PDF
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

# Main Execution
if st.button("Run Agents"):
    if not user_query.strip():
        st.warning("Please enter a query to proceed.")
    else:
        # Handle PDF input
        if uploaded_file is not None:
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_file_path = tmp_file.name

            with open(tmp_file_path, "rb") as f:
                document_text = extract_text_from_pdf(f)
        else:
            document_text = ""

        # Initialize the Crew
        manager_crew = Crew(
            agents=[document_agent, query_agent, research_agent],
            tasks=[manager_decision_task],
            process=Process.hierarchical,
            manager_agent=manager_agent,
            memory=False,
            verbose=True
        )

        with st.spinner("Agents working on your request..."):
            result = manager_crew.kickoff(inputs={
                "user_input": user_query,
                "document": document_text.strip()
            })
            

        st.success("✅ Task Completed!")
        st.subheader("Response from Manager Agent")
        st.success("✅ Task Completed!")
        st.subheader("Response from Manager Agent")

        # unwrap CrewAI metadata
        if isinstance(result, dict) and "raw" in result:
            clean_json = json.loads(result["raw"])
        elif isinstance(result, dict) and "tasks_output" in result:
            clean_json = json.loads(result["tasks_output"][0].raw)
        else:
            clean_json = result  # fallback

        st.json(clean_json)



