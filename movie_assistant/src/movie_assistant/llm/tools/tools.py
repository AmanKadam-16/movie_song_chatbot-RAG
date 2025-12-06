class ToolsList:
    TOOLS = [
        {
            "type": "function",
            "function": {
                "name": "rag_tool",
                "description": "Returns chunks of context based on Rephrased User Query received.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_query": {
                            "type": "string",
                            "description": "Rephrased version of user message to get relvant context and chunks.",
                        },
                    },
                    "required": ["user_query"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "web_search",
                "description": "Searches internet with the rephrased user query to fetch relevant result.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "search_query": {
                            "type": "string",
                            "description": "Rephrased version of user message to get relevant chunks of information.",
                        },
                    },
                    "required": ["search_query"],
                },
            },
        },
    ]
