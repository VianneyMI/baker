"""`baker.models.recipe` module."""

from pydantic import BaseModel
from baker.models.ingredient import Ingredient


class Recipe(BaseModel):
    """`baker.models.recipe.Recipe`class.

    Describes a recipe in a computer-friendly way.
    """

    title: str
    serving_size: int
    preparation_time: float
    cooking_time: float
    ingredients: list[Ingredient]
    directions_source_text: str
