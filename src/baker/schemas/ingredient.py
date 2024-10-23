"""`baker.schemas.ingredients` module."""

import ast
from fractions import Fraction

from pydantic import Field, field_validator
from baker.schemas.base import BaseBakerModel
from baker.schemas.range import Range
from baker.schemas.units import UnitEnum

class Ingredient(BaseBakerModel):
    """`baker.schemas.ingredient.Ingredient` class.
    
    Represents an ingredient used in a recipe.
    This class proposes a formal structure to describe an ingredient
    to make it more suitable for alrgorithmic processing.

    In particular, it includes a `quantity` and a `unit` fields that can be used
    by algorithms.
    
    """

    id: int = Field(
        description="Randomly generated unique identifier of the ingredient",
        examples=[1, 2, 3, 4, 5, 6],
    )
    name: str = Field(
        description="The name of the ingredient", examples=["flour", "sugar", "salt"]
    )
    quantity: float | Range | None = Field(
        None,
        description="The quantity of the ingredient. Range should be used only if the source text mentions a range of values.",
        examples=[200, 4, 0.5, {"min": 1, "max": 3}],
    )

    
    unit: UnitEnum | None = Field(
        None,
        description="The unit in which the quantity is specified",
        examples=["ml", "unit", "l", "unit", "teaspoon", "tablespoon"],
    )
    optional: bool = Field(False, description="Whether the ingredient is optional or not")

    @field_validator("quantity", mode="before")
    def parse_quantity(cls, value: float | int | str | None)->float|int|None:
        """
        Converts the quantity to a float if it is not already one.

        Arguments:
        ----------------------------
        value: float | int | str | None 
            The quantity value to be parsed.

        Returns:
            float | int | None: The parsed quantity as a float or int, or None if the input is invalid.
        """
        if isinstance(value, str):
            try:
                # Try to convert directly to float
                value = float(value)
            except ValueError:
                try:
                    # Try to evaluate as a fraction
                    value = float(Fraction(value))
                except ValueError:
                    try:
                        # Try to evaluate as a literal
                        value = ast.literal_eval(value)
                        if not isinstance(value, (int, float)):
                            raise ValueError("Parsed value is not a number")
                    except (ValueError, SyntaxError):
                        print("Invalid quantity format")
                        return None

        return value