from pydantic import BaseModel


class Step(BaseModel):
    """`baker.schemas.step.Step` class.

    Represents a step, an instruction in a recipe.
    This class proposes a formal structure to describe a step
    to make it more suitable for alrgorithmic processing.
    In particular, it extract numerical values like durations and temperatures
    """

    number: int
    description: str
