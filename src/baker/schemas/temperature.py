"""`baker.schemas.temperature` module."""

from baker.schemas.base import BaseBakerModel
from baker.schemas.range import Range


class Temperature(BaseBakerModel):
    """`baker.schemas.temperature.Temperature`class."""

    preheat : float | Range | None = None
    baking : float | Range | None = None
    cooking : float | Range | None = None
    cooling : float | Range | None = None
    