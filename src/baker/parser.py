""" `baker.parser` module"""

from langchain.output_parsers import PydanticOutputParser
from langchain.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_community.chat_models.openai import ChatOpenAI

from baker.settings import SETTINGS
from baker.schemas import Recipe, Ingredients

PROMPT_TEMPLATE = """
What are the ingredients and their associated quantities as well as the steps to make the recipe described by the following {ingredients} and {steps} provided as raw text ?

In particular, please provide the following information:
- The name of the recipe
- The serving size
- The ingredients and their associated quantities
- The steps to make the recipe
- Any additional comments
as described in {format_instructions}

"""


LLM = ChatOpenAI(openai_api_key=SETTINGS.openai_api_key, model=SETTINGS.openai_model)
MESSAGE = HumanMessagePromptTemplate.from_template(template=PROMPT_TEMPLATE)
CHAT_PROMPT_TEMPLATE = ChatPromptTemplate.from_messages(messages=[MESSAGE])
PARSER = PydanticOutputParser(pydantic_object=Ingredients)

class RecipeParser:

    def __init__(
            self,
            llm:ChatOpenAI=LLM,
            prompt_template:ChatPromptTemplate=CHAT_PROMPT_TEMPLATE,
            parser:PydanticOutputParser=PARSER
    )->None:
        self.llm = llm
        self.prompt_template = prompt_template
        self.parser = parser


    async def run(self, ingredients: str, steps:str|None=None) -> dict | Recipe| None:
        """Calls the llm to perform the parsing."""

        output = None

        try:
            if self.parser is not None:
                format_instructions = self.parser.get_format_instructions()
            else:
                format_instructions = ''

            chat_prompt = self.prompt_template.format_prompt(ingredients=ingredients, steps=steps, format_instructions=format_instructions)

            output = await self.llm.ainvoke(chat_prompt.to_messages())
            self._cache = output
            if self.parser is not None:
                output = self.parser.parse(output.content)
                self._cache = output
        except BaseException as e:
            print(e)
            try:
                output = output.content
            except:
                output = None

        return output
    