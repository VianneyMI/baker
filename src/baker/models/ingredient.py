"""`baker.models.ingredient` module."""

from pydantic import BaseModel
from baker.schemas.units import StandardUnitEnum


class Ingredient(BaseModel):
    """`baker.models.ingredient.Ingredient` class."""

    name: str
    quantity: float
    unit: StandardUnitEnum
    # NOTE: In a future version, we could set unit as a ParsingUnitEnum instance and dynamically convert it to a StandardUnitEnum instance.
