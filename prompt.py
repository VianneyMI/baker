"""`prompt.py`"""

from langchain_core.messages import BaseMessage
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate


DEFAULT_BASE_PROMPT = """
What are the ingredients and their associated quantities as well as the steps to make the recipe described by the following {ingredients} and {steps} provided as raw text ?

In particular, please provide the following information:
- The name of the recipe
- The serving size
- The ingredients and their associated quantities
- The steps to make the recipe and in particular, the duration of each step
- The total duration of the recipe broken down into preparation, cooking and waiting time. The totals must be consistent with the sum of the durations of the steps. 
- Any additional comments

{format_instructions}
Make sure to provide a valid and well-formatted JSON.

"""

def create_prompt(
        base_prompt: str,
        output_format: PydanticOutputParser,
        ingredients: str,
        steps: str | None = None
)->list[BaseMessage]:
    """Create a prompt for the model."""

    prompt_template = HumanMessagePromptTemplate.from_template(template=base_prompt)
    chat_prompt_template = ChatPromptTemplate.from_messages(messages=[prompt_template])
    format_instructions = output_format.get_format_instructions()


    chat_prompt = chat_prompt_template.format_prompt(
        ingredients=ingredients, 
        steps=steps, 
        format_instructions=format_instructions,
        )
    
    return chat_prompt.to_messages()