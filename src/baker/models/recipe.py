"""`baker.models.recipe` module."""

from pydantic import BaseModel
from baker.models.ingredient import Ingredient


class Recipe(BaseModel):
    """`baker.models.recipe.Recipe`class.

    Describes a recipe in a computer-friendly way.
    """

    title: str
    serving_size: int = 1
    preparation_time: float | None = None
    cooking_time: float | None = None
    ingredients: list[Ingredient]
    directions_source_text: str | None = None
