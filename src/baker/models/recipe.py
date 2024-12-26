"""`baker.models.recipe` module."""

from pydantic import BaseModel
from baker.schemas.range import Range
from baker.models.ingredient import Ingredient
from baker.models.step import Step


class Recipe(BaseModel):
    """`baker.models.recipe.Recipe`class.

    Describes a recipe in a computer-friendly way.
    """

    title: str
    original_serving_size: int | None = None
    serving_size: int | None = None
    preparation_time: float | Range | None = None
    cooking_time: float | Range | None = None
    ingredients: list[Ingredient]
    # directions_source_text: str | None = None
    steps: list[Step]
