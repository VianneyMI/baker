"""`core.py`"""

from typing import Any
from langchain.output_parsers import PydanticOutputParser
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage

async def run(
        llm:BaseChatModel,
        prompt:list[BaseMessage],
        parser:PydanticOutputParser
)->Any:
    
    _output = None
    output = None

    # Requesting LLM
    # ------------------
    try:    
        _output = await llm.ainvoke(prompt)
    except BaseException as e:
        print(f"Error in LLM communication {e}")

    # Parsing/Formatting the  output
    # ------------------
    try:
        if _output is not None:
            output = parser.parse(_output.content)
    except BaseException as e:
        print(f"Error in parsing {e}")

        # Backup in case parsing fails
        # --------------------------------
        if isinstance(_output, BaseMessage):
            output = _output.content
        

    return output
    