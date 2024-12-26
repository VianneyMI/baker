"""`baker.engine.core` module."""

import os
from dotenv import load_dotenv
import certifi
from pymongo import MongoClient
from pymongo.collection import Collection
from monggregate import Pipeline, S
from baker.models.ingredient import Ingredient


def get_recipes_collection() -> Collection:
    """Get the database connection."""

    load_dotenv()
    uri = os.getenv("MONGODB_SERVER")
    print(uri)
    client = MongoClient(uri, tlsCAFile=certifi.where())  # type: ignore
    db = client["baker"]
    recipes = db["recipes"]
    return recipes


def find_recipes(
    ingredients: list[Ingredient], serving_size: int = 1
) -> list[dict]:  # recipes
    """Find recipes."""

    # Get the recipes collection
    recipes = get_recipes_collection()

    # Create the pipeline
    pipeline = Pipeline()
    pipeline = include_normalization_steps(pipeline)
    query = generate_match_query(ingredients, serving_size)
    print(query)
    pipeline.match(query=query).project(
        include=[
            "id",
            "title",
            "preparation_time",
            "cooking_time",
            "serving_size",
            "ingredients",
            "directions_source_text",
        ],
        exclude="_id",
    )

    # Find the recipes
    result = recipes.aggregate(pipeline.export()).to_list(length=None)

    return result


def generate_match_query(ingredients: list[Ingredient], serving_size: int = 1) -> dict:
    """Generate the match query."""

    operands = []
    for ingredient in ingredients:
        operand = {
            "ingredients.name": ingredient.name,
            "ingredients.unit": ingredient.unit,
            "ingredients.quantity": {"$gte": ingredient.quantity / serving_size},
        }
        operands.append(operand)

    query = {"$and": operands}

    return query


def include_normalization_steps(pipeline: Pipeline):
    """Adds steps in a pipeline to normalize the ingredients quantity in the db

    The steps below normalize the quantities of the ingredients in the recipes in the DB by the recipe serving size.

    """

    # Unwind the ingredients
    pipeline.unwind(path="$ingredients")

    # Add the normalized quantity
    pipeline.add_fields(
        {
            "ingredients.quantity": S.divide(
                S.field("ingredients.quantity"), S.max([S.field("serving_size"), 1])
            )
        }
    )

    # Group the results
    pipeline.group(
        by="_id",
        query={
            "id": {"$first": "$id"},
            "title": {"$first": "$title"},
            "serving_size": {"$first": "$serving_size"},
            "preparation_time": {"$first": "$preparation_time"},
            "cooking_time": {"$first": "$cooking_time"},
            "directions_source_text": {"$first": "$directions_source_text"},
            "ingredients": {"$addToSet": "$ingredients"},
        },
    )
    return pipeline
