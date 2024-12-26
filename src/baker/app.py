"""Serve and render"""

from fastapi import FastAPI

from baker.engine.core import find_recipes
from baker.models.ingredient import Ingredient
from baker.models.recipe import Recipe

app = FastAPI()


@app.get("/")
def welcome():
    return {"message": "Welcome to the Baker API !"}


@app.post("/recipes")
def _find_recipes(ingredients: list[Ingredient], serving_size: int = 1) -> list[Recipe]:
    """Find recipes"""

    return find_recipes(ingredients, serving_size)  # type: ignore
