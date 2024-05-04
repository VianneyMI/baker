"""`baker.schemas` module"""


from pydantic import BaseModel, Field, field_validator


class Ingredient(BaseModel):
    """Ingredient schema"""

    name: str = Field(description="The name of the ingredient", examples=["flour", "sugar", "salt"])
    quantity:float | None = Field(None, description="The quantity of the ingredient", examples=[200, 4, 0.5, 1, 1, 1 ])
    unit: str | None = Field(None, description="The unit in which the quantity is specified", examples=["ml", "unit", "l", "unit", "teaspoon", "tablespoon"])

    @field_validator("quantity", mode="before")
    def parse_quantity(cls, value:float|int|str|None):
        """Converts the quantity to a float if it is not already one"""
        
        if isinstance(value, str):
            try:
                value = float(value)
            except ValueError:
                try:
                    value = eval(value)
                except:
                    pass

        return value
        
class Ingredients(BaseModel):
    """Ingredients schema"""

    ingredients: list[Ingredient] = []
    


class Recipe(BaseModel):
    """Recipe schema"""

    name: str = Field(description="The name of the recipe", examples=["Chocolate Cake", "Apple Pie", "Pasta Carbonara", "Pumpkin Soup", "Chili con Carne"])
    serving_size: int | None = Field(None, description="The number of servings the recipe makes", examples=[1, 2, 4, 6, 8, 10])
    ingredients: list[Ingredient] = []
    steps: list[str] = []
    comments: list[str] = []
    

if __name__ == "__main__":
    
    ingredient = Ingredient(name="flour", quantity="null", unit="g")
    print(ingredient)
    print(type(ingredient.quantity))
