from movie_assistant.llm.tools.tool_functions import rag_search, web_search


class ToolRegistory:

    TOOL_MAPPING = {"rag_tool": rag_search, "web_search": web_search}
