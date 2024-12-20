"""`baker.engine.core` module."""

from pymongo import MongoClient
from pymongo.collection import Collection
from monggregate import Pipeline, S
from baker.models.ingredient import Ingredient


def get_recipes_collection() -> Collection:
    """Get the database connection."""

    client = MongoClient("mongodb://localhost:27017/")
    db = client["baker"]
    recipes = db["recipes"]
    return recipes


def find_recipes(ingredients: list[Ingredient]) -> dict:  # recipes
    """Find recipes."""

    # Get the recipes collection
    recipes = get_recipes_collection()

    # Create the pipeline
    pipeline = Pipeline()

    # Find the recipes
    result = recipes.aggregate(pipeline)

    return result
