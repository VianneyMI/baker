"""`baker.schemas.step` module."""

from pydantic import Field
from baker.schemas.base import BaseBakerModel
from baker.schemas.duration import Duration
from baker.schemas.temperature import Temperature
from baker.schemas.intensity import Intensity

class Step(BaseBakerModel):
    """`baker.schemas.step.Step` class.
    
    Represents a step, an instruction in a recipe.
    This class proposes a formal structure to describe a step
    to make it more suitable for alrgorithmic processing.
    In particular, it extract numerical values like durations and temperatures
    """
    
    number: int | None = Field(
        None,
        description="The position of the step in the recipe",
        examples=[1, 2, 3, 4, 5, 6],
    )
    description: str = Field(
        description="The action that needs to be performed during that step",
        examples=[
            "Preheat the oven to 180°C",
            "Mix the flour and sugar in a bowl",
            "Add the eggs and mix well",
            "Pour the batter into a greased cake tin",
            "Bake for 30 minutes",
            "Let the cake cool down before serving",
        ],
    )
    duration: Duration | None = Field(None, description="The duration of the step broken down by broad category of cooking action.")
    temperature: Temperature|None = Field(None, description="The temperature of the step broken down by broad category of cooking action.")
    heat_intensity : Intensity | str | None = Field(None, description="The heat intensity of the step")
    ingredients_ids: list[int] = Field(
        [],
        description="The list of ingredient ids used in the step",
        examples=[[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12]],
    )
    optional:bool = Field(False, description="Whether the ingredient is optional or not")