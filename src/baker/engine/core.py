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


def find_recipes(ingredients: list[Ingredient]) -> list[dict]:  # recipes
    """Find recipes."""

    # Get the recipes collection
    recipes = get_recipes_collection()

    # Create the pipeline
    pipeline = Pipeline()
    query = generate_match_query(ingredients)
    # TODO: Omitting normalization for now
    pipeline.match(query=query)

    # Find the recipes
    result = recipes.aggregate(pipeline.export()).to_list(length=None)

    return result


def generate_match_query(ingredients: list[Ingredient]) -> dict:
    """Generate the match query."""

    operands = []
    for ingredient in ingredients:
        operand = {
            "ingredients.name": ingredient.name,
            "ingredients.unit": ingredient.unit,
            "ingredients.quantity": S.lte(
                S.field("ingredients.quantity"), ingredient.quantity
            ),
        }
        operands.append(operand)

    query = {"$and": operands}

    return query
