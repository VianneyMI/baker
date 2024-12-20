"""Serve and render"""

from fastapi import FastAPI

from baker.engine.core import find_recipes
from baker.models.ingredient import Ingredient

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/recipes")
def _find_recipes(ingredients: list[Ingredient]) -> list[dict]:
    """Find recipes"""

    return find_recipes(ingredients)
