# agent.py
from crewai import Agent, LLM
from crewai_tools import SerperDevTool, FileReadTool
from crewai.tools import BaseTool
import os

# Initialize LLM
llm = LLM(
    model="gpt-4.1-mini"
)

# Custom tool for document analysis
class DocumentAnalysisTool(BaseTool):
    name: str = "Document Analysis Tool"
    description: str = "Analyzes documents for summarization and keyword extraction"

    def _run(self, document_content: str) -> str:
        words = document_content.lower().split()
        stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an',
                      'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does',
                      'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that',
                      'these', 'those'}
        word_freq = {}
        for word in words:
            word = word.strip('.,!?;:"()[]{}')
            if word not in stop_words and len(word) > 3:
                word_freq[word] = word_freq.get(word, 0) + 1
        keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        return str([word for word, freq in keywords])

# Tools
serper_dev_tool = SerperDevTool()
file_read_tool = FileReadTool()
document_analysis_tool = DocumentAnalysisTool()

# Agent 1: Document Summarizer and Keyword Extractor
document_agent = Agent(
    role="Document Analyst",
    goal="Summarize documents and extract the most important keywords",
    backstory=(
        "As an expert document analyst, you excel at reading through complex documents "
        "and distilling them into clear, concise summaries. You have a keen eye for "
        "identifying the most important keywords and themes that capture the essence "
        "of any document. Your summaries are always structured and actionable."
    ),
    allow_delegation=False,
    llm=llm

)

# Agent 2: Query Responder
query_agent = Agent(
    role="Query Specialist",
    goal="Answer user questions based on provided documents with accuracy and clarity",
    backstory=(
        "You are a knowledgeable query specialist who excels at understanding user questions "
        "and finding the most relevant information from available documents. You provide "
        "clear, comprehensive answers that directly address what users are asking for. "
        "You always stay within the bounds of the provided information."
    ),
    allow_delegation=False,
    llm=llm
)

# Agent 3: Internet-Connected Research Agent
research_agent = Agent(
    role="Research Specialist",
    goal="Fetch current and accurate information from the internet",
    backstory=(
        "You are a skilled research specialist with access to real-time internet data. "
        "You excel at finding the most current, relevant, and credible information online. "
        "You always provide proper source attribution and focus on delivering accurate, "
        "up-to-date answers to user queries."
    ),
    allow_delegation=False,
    llm=llm
)

# Agent 4: Manager Agent
manager_agent = Agent(
    role="Task Manager",
    goal="Analyze user requests and route them to the most appropriate specialized agents",
    backstory=(
        "You are an intelligent task manager with deep understanding of each specialist's "
        "capabilities. You analyze incoming requests, determine which agent or combination "
        "of agents would best handle each task, and provide clear justification for your "
        "routing decisions. You ensure efficient task distribution and optimal outcomes."
    ),
    allow_delegation=True,
    llm=llm
)


# # Export objects
# __all__ = [
#     "llm",
#     "document_agent",
#     "query_agent",
#     "research_agent",
#     "manager_agent",
#     "serper_dev_tool",
#     "file_read_tool",
#     "document_analysis_tool"
# ]
