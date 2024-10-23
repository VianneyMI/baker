"""`baker.schemas.range` module."""

from pydantic import Field
from baker.schemas.base import BaseBakerModel

class Range(BaseBakerModel):
    """`baker.schemas.range.Range` class.
    
    Represents a range of numerical values.
    This range can describe duration ranges, temperature ranges, etc.

    `Range`should be used only if the source text mentions a range of values.
    """

    min: float|None = Field(
        None,
        description="The start of the range",
        examples=[1, 2, 3, 4, 5, 6],
    )
    max: float|None = Field(
        None,
        description="The end of the range",
        examples=[1, 2, 3, 4, 5, 6],
    )
