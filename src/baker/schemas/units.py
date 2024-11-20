"""`baker.schemas.unit` module."""

from enum import StrEnum

class UnitEnum(StrEnum):
    """`baker.schemas.unit.UnitEnum` enum.
    
    Enumeration of common units of measurement used in recipes.
    """

    NA = "N/A"
    UNKNOWN = "unknown"
    # Volume units
    ML = "ml"
    L = "l"
    TEASPOON = "teaspoon"
    TABLESPOON = "tablespoon"
    CUP = "cup"
    PINT = "pint"
    QUART = "quart"
    GALLON = "gallon"
    LITER = "liter"
    MILLILITER = "milliliter"
    FLUID_OUNCE = "fluid_ounce"
    DASH = "dash"
    DROP = "drop"
    PINCH = "pinch"
    JIGGER = "jigger"
    SHOT = "shot"

    # Weight units
    GRAM = "gram"
    KILOGRAM = "kilogram"
    OUNCE = "ounce"
    POUND = "pound"
    MILLIGRAM = "milligram"
    STONE = "stone"

    # Miscellaneous units
    UNIT = "unit"
    SLICE = "slice"
    PIECE = "piece"
    BUNCH = "bunch"
    STICK = "stick"
    CAN = "can"
    PACKAGE = "package"
    BAG = "bag"
    BOX = "box"
    CONTAINER = "container"
    BOTTLE = "bottle"
    JAR = "jar"
    TUBE = "tube"
    SPRIG = "sprig"
    CLOVE = "clove"
    FILLET = "fillet"
    HEAD = "head"
    BULB = "bulb"
    LEAF = "leaf"
    RIB = "rib"
    SLAB = "slab"
    LOAF = "loaf"
    SHEET = "sheet"
    ROLL = "roll"
    BAR = "bar"
    BLOCK = "block"
    WEDGE = "wedge"
    RING = "ring"
    LINK = "link"
    STRIP = "strip"
    