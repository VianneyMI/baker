"""`baker.schemas.action` module."""

from enum import StrEnum

class CookingActionsEnum(StrEnum):
    """`baker.schemas.action.CookingActionsEnum` enum.
    
    Enumeration of common actions undertook while cooking.
    """

    PREPARATION = "preparation"
    COOKING = "cooking"
    WAITING = "waiting"