"""`baker.schemas` module"""


from pydantic import BaseModel, Field, field_validator


class Ingredient(BaseModel):
    """Ingredient schema"""

    id : int = Field(description="Randomly generated unique identifier of the ingredient", examples=[1, 2, 3, 4, 5, 6])
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
                except Exception as e:
                    print(e)
                    pass

        return value
        
class Ingredients(BaseModel):
    """Ingredients schema"""

    ingredients: list[Ingredient] = []


class Step(BaseModel):

    number : int|None = Field(None, description="The position of the step in the recipe", examples=[1, 2, 3, 4, 5, 6])
    description: str = Field(description="The action that needs to be performed during that step", examples=["Preheat the oven to 180°C", "Mix the flour and sugar in a bowl", "Add the eggs and mix well", "Pour the batter into a greased cake tin", "Bake for 30 minutes", "Let the cake cool down before serving"])
    preparation_time: int|None = Field(None, description="The preparation time mentioned in the step description if any.", examples=[5, 10, 15, 20, 25, 30])
    cooking_time: int|None = Field(None, description="The cooking time mentioned in the step description if any.", examples=[5, 10, 15, 20, 25, 30])
    used_ingredients: list[int] = Field([], description="The list of ingredient ids used in the step", examples=[[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12]])


class Recipe(BaseModel):
    """Recipe schema"""

    name: str = Field(description="The name of the recipe", examples=["Chocolate Cake", "Apple Pie", "Pasta Carbonara", "Pumpkin Soup", "Chili con Carne"])
    serving_size: int | None = Field(None, description="The number of servings the recipe makes", examples=[1, 2, 4, 6, 8, 10])
    ingredients: list[Ingredient] = []
    steps: list[Step] = []
    total_preparation_time: int | None = Field(None, description="The total preparation time for the recipe", examples=[5, 10, 15, 20, 25, 30])
    total_cooking_time: int | None = Field(None, description="The total cooking time for the recipe", examples=[5, 10, 15, 20, 25, 30])
    comments: list[str] = []
    

if __name__ == "__main__":
    
    ingredient = Ingredient(name="flour", quantity="null", unit="g")
    print(ingredient)
    print(type(ingredient.quantity))
