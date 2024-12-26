import streamlit as st
from typing import List
import requests
import json

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


def display_recipe(recipe: dict):
    """Display a single recipe in a nice format"""
    with st.expander(f"📖 {recipe['title']}", expanded=True):
        # Recipe times
        col1, col2 = st.columns(2)
        with col1:
            st.write("⏲️ Preparation:", f"{recipe['preparation_time']} min")
        with col2:
            st.write("🍳 Cooking:", f"{recipe['cooking_time']} min")

        # Ingredients
        st.write("🧂 **Ingredients:**")
        for ing in recipe["ingredients"]:
            st.write(f"- {ing['quantity']} {ing['unit']} {ing['name']}")

        # Instructions
        st.write("📝 **Instructions:**")
        st.write(recipe["directions_source_text"])


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
