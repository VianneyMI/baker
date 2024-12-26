import streamlit as st
from typing import List
import requests

from baker.models.ingredient import Ingredient
from baker.schemas.units import StandardUnitEnum


def create_ingredient_input(index: int):
    """Create input fields for a single ingredient"""
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        name = st.text_input(f"Ingredient name", key=f"name_{index}")
    with col2:
        quantity = st.number_input(
            f"Quantity", min_value=0.0, step=0.1, key=f"quantity_{index}"
        )
    with col3:
        unit = st.selectbox(
            f"Unit",
            options=[unit.value for unit in StandardUnitEnum],
            key=f"unit_{index}",
        )

    return name, quantity, unit


def call_recipes_api(ingredients: List[Ingredient], serving_size: int) -> List[dict]:
    """Make API call to the FastAPI backend"""
    API_URL = "http://localhost:8000/recipes"

    try:
        # Convert ingredients to JSON-serializable format
        ingredients_json = [ing.model_dump() for ing in ingredients]

        response = requests.post(
            API_URL,
            json=ingredients_json,
            params={"serving_size": serving_size},
        )

        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return []

    except requests.exceptions.ConnectionError:
        st.error(
            "Could not connect to the API. Make sure the FastAPI server is running."
        )
        return []
    except Exception as e:
        st.error(f"Error calling API: {str(e)}")
        return []


def format_time(time_value) -> str:
    """Format time values, handling None, integers, and ranges"""
    if time_value is None:
        return "N/A"
    elif isinstance(time_value, (int, float)):
        # Format float to 2 decimal places, remove trailing zeros
        return f"{float(f'{time_value:.2f}'):g} min"
    elif isinstance(time_value, dict) and "min" in time_value and "max" in time_value:
        # Format both min and max values
        min_val = float(f"{time_value['min']:.2f}")
        max_val = float(f"{time_value['max']:.2f}")
        return f"{min_val:g}-{max_val:g} min"
    return "N/A"


def format_quantity(quantity: float) -> str:
    """Format quantity to display at most 2 decimal places"""
    # Convert to float with 2 decimal places, remove trailing zeros
    return f"{float(f'{quantity:.2f}'):g}"


def capitalize_first_letter(text: str) -> str:
    """Capitalize first letter of text only if it starts with a letter"""
    if text and text[0].isalpha():
        return text[0].upper() + text[1:]
    return text


def display_recipe(recipe: dict):
    """Display a single recipe in a nice format"""
    with st.expander(f"📖 {recipe['title']}", expanded=True):
        # Recipe metadata
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("⏲️ Preparation:", format_time(recipe["preparation_time"]))
        with col2:
            st.write("🍳 Cooking:", format_time(recipe["cooking_time"]))
        with col3:
            total_time = 0
            if isinstance(recipe["preparation_time"], (int, float)):
                total_time += recipe["preparation_time"]
            if isinstance(recipe["cooking_time"], (int, float)):
                total_time += recipe["cooking_time"]
            if total_time > 0:
                st.write("⌛ Total time:", format_time(total_time))
            else:
                st.write("⌛ Total time:", "N/A")

        # Serving size if available
        if recipe.get("serving_size"):
            st.write("👥 **Serves:** ", recipe["serving_size"])

        # Ingredients with better formatting
        st.write("🧂 **Ingredients:**")
        ingredients_list = ""
        for ing in recipe["ingredients"]:
            quantity = format_quantity(ing["quantity"])
            # Only include unit if it's not "unit"
            if ing["unit"].lower() == "unit":
                ingredients_list += f"- {quantity} {ing['name']}\n"
            else:
                ingredients_list += f"- {quantity} {ing['unit']} {ing['name']}\n"
        st.markdown(ingredients_list)

        # Instructions with better formatting
        if recipe.get("steps"):
            st.write("📝 **Instructions:**")
            steps_list = ""
            for step in recipe["steps"]:
                # Each step is a dictionary with 'number' and 'description' fields
                if step["description"].strip():  # Only show non-empty steps
                    description = capitalize_first_letter(step["description"].strip())
                    steps_list += f"{step['number']}. {description}\n"
            st.markdown(steps_list)


def add_buy_me_coffee_button():
    """Add Buy Me a Coffee button to the sidebar"""
    st.sidebar.markdown(
        """
        <a href="https://www.buymeacoffee.com/vianmixt" target="_blank">
            <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" 
                 alt="Buy Me A Coffee" 
                 style="height: 60px; width: 217px;">
        </a>
        """,
        unsafe_allow_html=True,
    )


def main():
    st.title("Recipe Finder")

    # Add Buy Me a Coffee button in the sidebar
    add_buy_me_coffee_button()

    # Initialize session state for number of ingredients
    if "num_ingredients" not in st.session_state:
        st.session_state.num_ingredients = 3

    # Number of ingredients input (outside the form)
    num_ingredients = st.number_input(
        "Number of ingredients",
        min_value=1,
        max_value=5,
        value=st.session_state.num_ingredients,
        key="ingredient_count",
    )

    # Update session state when Enter is pressed
    if num_ingredients != st.session_state.num_ingredients:
        st.session_state.num_ingredients = num_ingredients

    # Form for ingredients and submission
    with st.form("recipe_finder_form"):
        st.subheader("Ingredients")

        # Container for ingredient inputs
        ingredients_data = []
        for i in range(st.session_state.num_ingredients):
            st.markdown(f"**Ingredient {i + 1}**")
            name, quantity, unit = create_ingredient_input(i)
            ingredients_data.append((name, quantity, unit))

        # Serving size
        st.subheader("Serving Size")
        serving_size = st.number_input("Number of servings", min_value=1, value=1)

        # Submit button
        submitted = st.form_submit_button("Find Recipes")

        if submitted:
            # Create list of Ingredient objects
            ingredients = []
            for name, quantity, unit in ingredients_data:
                if name.strip():  # Only include ingredients with a name
                    try:
                        ingredient = Ingredient(
                            name=name.strip().lower(),
                            quantity=quantity,
                            unit=StandardUnitEnum(unit),
                        )
                        ingredients.append(ingredient)
                    except ValueError as e:
                        st.error(f"Invalid ingredient data: {e}")
                        break

            if ingredients:
                with st.spinner("Searching for recipes..."):
                    recipes = call_recipes_api(ingredients, serving_size)

                if recipes:
                    st.success(f"Found {len(recipes)} recipes!")
                    for recipe in recipes:
                        display_recipe(recipe)
                else:
                    st.warning("No recipes found with these ingredients.")


if __name__ == "__main__":
    main()
