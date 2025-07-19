# # app.py

from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from crewai import Crew, Process
from agents_config import document_agent, query_agent, research_agent, manager_agent
from agent_task import manager_decision_task
from pypdf import PdfReader
import tempfile
import json
import os
from typing import Optional
from typing import Union

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AI Agent Crew API",
    description="Intelligent Document & Query Assistant",
    version="1.0.0"
)

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

@app.post("/process-query")
async def process_query(
    query: str = Form(...),
    file: Union[UploadFile, str, None] = File(default=None)
):
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    try:
        document_text = ""

        # ✅ Handle only real file uploads (not empty string from Swagger)
        if isinstance(file, UploadFile) and file.filename:
            if file.filename.endswith(".pdf"):
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    tmp_file.write(await file.read())
                    tmp_file_path = tmp_file.name

                with open(tmp_file_path, "rb") as f:
                    document_text = extract_text_from_pdf(f)

                os.unlink(tmp_file_path)

        # Run Crew
        manager_crew = Crew(
            agents=[document_agent, query_agent, research_agent],
            tasks=[manager_decision_task],
            process=Process.hierarchical,
            manager_agent=manager_agent,
            memory=False,
            verbose=True
        )

        result = manager_crew.kickoff(inputs={
            "user_input": query,
            "document": document_text.strip()
        })

        from json import loads
        if hasattr(result, "raw") and result.raw:
            clean_result = loads(result.raw)
        elif hasattr(result, "tasks_output") and result.tasks_output:
            clean_result = loads(result.tasks_output[0].raw)
        else:
            clean_result = {"output": str(result)}

        return JSONResponse(content=clean_result)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})
