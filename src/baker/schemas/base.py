"""`baker.schemas.base` module."""

from pydantic import BaseModel, ConfigDict

class BaseBakerModel(BaseModel):
    """`baker.schemas.base.BaseBakerModel` class.
    
    Parent class for all Pydantic models in the `baker` package.
    """

    model_config = ConfigDict(populate_by_name=True)
