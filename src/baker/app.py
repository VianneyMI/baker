"""Serve and render"""

from fastapi import FastAPI

from baker.engine.core import find_recipes
from baker.models.ingredient import Ingredient
from baker.models.recipe import Recipe
from baker.logging import log_request_response_to_db

app = FastAPI()


@app.get("/")
def welcome():
    return {"message": "Welcome to the Baker API !"}


@app.post("/recipes")
def _find_recipes(ingredients: list[Ingredient], serving_size: int = 1) -> list[Recipe]:
    """Find recipes"""

    results = find_recipes(ingredients, serving_size)
    try:
        log_request_response_to_db(ingredients, serving_size, results)
    except Exception as e:
        print(f"Error logging request and response to database: {e}")

    return results
