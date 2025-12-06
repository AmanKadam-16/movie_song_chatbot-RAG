from sqlalchemy.orm import Session
from movie_assistant.core.llm.llm_client import LLM
from movie_assistant.llm.tools.tools import ToolsList
from movie_assistant.llm.tools.tool_registory import ToolRegistory
from movie_assistant.llm.prompt_template import Prompts
from movie_assistant.core.config import settings
from movie_assistant.schemas.chatbot import ChatInput
from movie_assistant.schemas.app_enums import ChatRole
import json

CHAT_MEMORY = {}


def conversate(user_input: ChatInput, db: Session):
    client = LLM.get_client()

    system_prompt = Prompts.AGENTIC_PROMPT.format(MODEL_CONTEXT="N/A")
    system_object = {"role": ChatRole.SYSTEM.value, "content": system_prompt}
    user_object = {"role": ChatRole.USER.value, "content": user_input.prompt}
    session_id = user_input.session_id
    if session_id not in CHAT_MEMORY:
        CHAT_MEMORY[session_id] = []
        CHAT_MEMORY[session_id].append(system_object)
    CHAT_MEMORY[session_id].append(user_object)

    completion = client.chat.completions.create(
        model=settings.CHAT_MODEL_NAME,
        messages=CHAT_MEMORY[session_id],
        temperature=0.3,
        top_p=1,
        tools=ToolsList.TOOLS,
        tool_choice="auto",
        max_tokens=4096,
    )
    print(completion)
    print(completion.choices[0])
    tool_calls = completion.choices[0].message.tool_calls
    while tool_calls:
        if completion.choices[0].message.tool_calls:
            for tool_call in tool_calls:
                fn_name = tool_call.function.name
                fn_arg = json.loads(tool_call.function.arguments)
                print(f"Function Name {fn_name}")
                print(f"Function Argument {fn_arg}")
                invoke_fn = ToolRegistory.TOOL_MAPPING.get(fn_name)
                tool_response = invoke_fn(fn_arg)
                tool_object = {
                    "role": "tool",
                    "name": fn_name,
                    "content": json.dumps(tool_response),
                    "tool_call_id": tool_call.id,
                }
                system_prompt = Prompts.AGENTIC_PROMPT.format(MODEL_CONTEXT=tool_object)
                system_object = {
                    "role": ChatRole.SYSTEM.value,
                    "content": system_prompt,
                }
                CHAT_MEMORY[session_id][0] = system_object
        completion = client.chat.completions.create(
            model=settings.CHAT_MODEL_NAME,
            messages=CHAT_MEMORY[session_id],
            temperature=1,
            top_p=1,
            tools=ToolsList.TOOLS,
            tool_choice="auto",
            max_tokens=4096,
        )
        tool_calls = completion.choices[0].message.tool_calls
    if completion.choices[0].message.content:
        assistant_response = completion.choices[0].message.content
        print(f"Assistant Response {assistant_response}")
        return json.loads(assistant_response)
