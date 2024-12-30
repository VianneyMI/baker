import os
import certifi
from datetime import datetime
from pymongo import MongoClient
from pymongo.collection import Collection
from dotenv import load_dotenv

from baker.models.ingredient import Ingredient


def get_logs_collection() -> Collection:
    """Get the database connection."""

    load_dotenv()
    uri = os.getenv("MONGODB_SERVER")

    client = MongoClient(uri, tlsCAFile=certifi.where())  # type: ignore
    db = client["baker"]
    logs = db["logs"]
    return logs


def log_request_response_to_db(
    ingredients: list[Ingredient], serving_size: int, results: list[dict]
) -> None:
    """Log the request and response to the database"""

    # Keep only recipe id and name
    results = [
        {"id": recipe.get("id"), "name": recipe.get("name")} for recipe in results
    ]

    # Log the request and response to the database
    logs = get_logs_collection()
    logs.insert_one(
        {
            "timestamp": datetime.now(),
            "serving_size": serving_size,
            "ingredients": ingredients,
            "results": results,
        }
    )
