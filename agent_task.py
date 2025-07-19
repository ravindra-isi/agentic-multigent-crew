# task.py
from crewai import Task
from agents_config import document_agent, query_agent,research_agent, manager_agent,serper_dev_tool,file_read_tool,document_analysis_tool


# Task 1: Document Analysis Task
document_analysis_task = Task(
    description=(
        "Analyze the provided document content: {document_content}. "
        "Create a comprehensive summary that captures the main points, key themes, "
        "and important insights. Extract the most relevant keywords that represent "
        "the core concepts in the document."
    ),
    expected_output=(
        "Return a JSON response in exactly this format: "
        '{"document_summary": "Your detailed summary of the document", '
        '"keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"]}'
    ),
    tools=[document_analysis_tool],
    agent=document_agent
)

# Task 2: Query Response Task
query_response_task = Task(
    description=(
        "Answer the user query: '{query}' based on the provided documents: {documents}. "
        "Provide a comprehensive and accurate answer using only the information "
        "available in the given documents. If the information is not available "
        "in the documents, return None to indicate that the document does not provide "
        "an answer to the query."
    ),
    expected_output=(
        "Return a JSON response in exactly this format: "
        '{"query": "The original user query", '
        '"response": "Your comprehensive answer based on the provided documents or None if not answerable"}'
    ),
    tools=[file_read_tool],
    agent=query_agent
)

# Task 3: Internet Research Task
internet_research_task = Task(
    description=(
        "Research the query: '{query}' using internet search capabilities. "
        "Find the most current, relevant, and credible information available online. "
        "Provide a comprehensive answer with proper source attribution."
    ),
    expected_output=(
        "Return a JSON response in exactly this format: "
        '{"query": "The original user query", '
        '"response": "Your research-based answer with current information", '
        '"source": "URL or description of the information source"}'
    ),
    tools=[serper_dev_tool],
    agent=research_agent
)

# Task 2: Manager decision Task

manager_decision_task = Task(
    description=(
        "Analyze the user request: '{user_input}' and '{document}' and determine which specialized agent(s) "
        "should handle this task. The conditions to consider are as follows:\n"
        "- If the document: '{document}' is either not provided or provided as an empty string (document == '' ), the Manager Agent will directly route the task to Agent 3 (Research Specialist) to search for the answer online."
        "- If a document is provided (not an empty string), the first step is to call Agent 1 (Document Analyzer) for summarization and keyword extraction.\n"
        "- If both the document and the query are provided, analyze if the query can be answered using the document. If the answer can be derived from the document, call Agent 2 (Query Responder) to respond to the user's query using information from the document.\n"
        "- If Agent 2 returns None, meaning the query cannot be answered from the document, directly call Agent 3 (Research Specialist) to fetch the answer from real-time internet sources.\n"
        "- If no document is provided or the document is an empty string, directly call Agent 3 (Research Specialist) to search for the answer online.\n"
        "Provide clear reasoning for your agent selection decision based on the above conditions."
    ),
    expected_output=(
        "Return a JSON response in exactly this format: "
        '{ "manager_agent": { "decision": "Clear explanation of why you selected these agents.", '
        '"selected_agents": ["Agent1", "Agent2", "Agent3"] }, '
        '"agent_responses": { '
        '"Agent1": { "status": "status_code", "data": { "document_summary": "Summarized content of the document.", "keywords": ["keyword1", "keyword2"] } }, '
        '"Agent2": { "status": "status_code", "data": { "query": "Original user query", "response": "The answer derived from the provided docs or None" } }, '
        '"Agent3": { "status": "status_code", "data": { "query": "Original user query", "response": "The real-time answer fetched from the internet.", "source": "URL or source of the fetched information" } } } }'
    ),
    agent=manager_agent
)
