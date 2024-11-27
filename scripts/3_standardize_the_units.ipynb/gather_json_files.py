"""Script to gather all JSON files in a directory and combine them into a single JSON file."""

import json
import glob
from pathlib import Path

# Step 1: Get all the JSON file paths
file_paths = glob.glob(
    str(
        Path(__file__).parents[2]
        / "data"
        / "output"
        / "2_update_the_extraction_results"
        / "main_run"
    )
    + "/*.json"
)

# Step 2: Load each JSON document and add to a list
json_documents = []
for file_path in file_paths:
    with open(file_path, "r") as file:
        data = json.load(file)
        json_documents.append(data)

# Step 3: Save the list of JSON documents as a single JSON array
output_path = (
    Path(__file__).parents[2]
    / "data"
    / "output"
    / "3_standardize_the_data"
    / "parsed_recipes.json"
)
with open(output_path, "w") as output_file:
    json.dump(json_documents, output_file, indent=4)

print(f"Bundled JSON saved to {output_path}")
