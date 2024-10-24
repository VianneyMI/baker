"""`baker.schemas.recipe` module."""

import datetime
from pydantic import Field
from baker.schemas.base import BaseBakerModel
from baker.schemas.ingredient import Ingredient
from baker.schemas.step import Step
from baker.schemas.range import Range


class ParsedRecipe(BaseBakerModel):
    """`baker.schemas.recipe.ParsedRecipe`class.
    
    Describes a recipe main components, i.e its `ingredients` and `steps` in a computer friendly way.
    The `ingredients` and `steps` are structured in a way to extract essential information from the fluff.
    In particular, the `Ingredient`and `Step`classes highlight numerical values for durations and temperature. 
    """

    serving_size: int | None = Field(description="The number of servings the recipe makes.")
    preparation_time: float | Range | None = Field(None, description="The time (in minutes) it takes to prepare the recipe.")
    cooking_time: float | Range | None = Field(None, description="The time (in minutes) it takes to cook the recipe.")
    ingredients:list[Ingredient] = Field(default_factory=list, description="A list of ingredients used in the recipe.")
    steps:list[Step] = Field(default_factory=list, description="A list of steps to follow to make the recipe.")


class Recipe(ParsedRecipe):
    """`baker.schemas.recipe.Recipe`class.
    
    Describes a recipe in a computer-friendly way.
    """

    title: str = Field(description="The title of the recipe.")
    date: datetime.date | str = Field(description="The date the recipe was created.")
    tags: list[str] = Field(default_factory=list, description="A list of tags used to caegorize a recipe.")
    introduction:str|None = Field(None, description="A brief introduction to the recipe.")
    ingredients_source_text : str|None = None
    directions_source_text : str|None = None


