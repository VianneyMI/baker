"""`baker.schemas.duration` module."""

from baker.schemas.base import BaseBakerModel
from baker.schemas.range import Range

class Duration(BaseBakerModel):
    """`baker.schemas.duration.Duration` class.
    
    Represents time durations of an instruction in a recipe.
    The durations are categorized into preparation, cooking, and waiting.
    The time are described by a single numerical value whenever possible.
    Range should be used only if the source text mentions a range of values.
    """

    preparation : float | Range | None = None
    cooking : float | Range | None = None
    waiting : float | Range | None = None
