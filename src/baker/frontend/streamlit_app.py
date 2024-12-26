import streamlit as st
from typing import List
import requests

from baker.models.ingredient import Ingredient
from baker.schemas.units import StandardUnitEnum


def create_ingredient_input(index: int):
    """Create input fields for a single ingredient"""
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        name = st.text_input("Ingredient name", key=f"name_{index}")
    with col2:
        quantity = st.number_input(
            "Quantity", min_value=0.0, step=0.1, key=f"quantity_{index}"
        )
    with col3:
        unit = st.selectbox(
            "Unit",
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
        st.markdown(
            f"<div class='recipe-title'>{recipe['title']}</div>", unsafe_allow_html=True
        )

        # Create a container for better spacing
        with st.container():
            # Recipe metadata with better layout
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(
                    f"<div style='text-align: center;'>"
                    f"<p style='color: #666;'>⏲️ Preparation</p>"
                    f"<p style='font-size: 1.2rem;'>{format_time(recipe['preparation_time'])}</p>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
            with col2:
                st.markdown(
                    f"<div style='text-align: center;'>"
                    f"<p style='color: #666;'>🍳 Cooking</p>"
                    f"<p style='font-size: 1.2rem;'>{format_time(recipe['cooking_time'])}</p>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
            with col3:
                total_time = 0
                if isinstance(recipe["preparation_time"], (int, float)):
                    total_time += recipe["preparation_time"]
                if isinstance(recipe["cooking_time"], (int, float)):
                    total_time += recipe["cooking_time"]
                st.markdown(
                    f"<div style='text-align: center;'>"
                    f"<p style='color: #666;'>⌛ Total Time</p>"
                    f"<p style='font-size: 1.2rem;'>{format_time(total_time) if total_time > 0 else 'N/A'}</p>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

        # Rest of display_recipe remains similar but with styled headers
        st.markdown(
            "<div class='section-header'>🧂 Ingredients</div>", unsafe_allow_html=True
        )
        ingredients_list = ""
        for ing in recipe["ingredients"]:
            quantity = format_quantity(ing["quantity"])
            # Only include unit if it's not "unit"
            if ing["unit"].lower() == "unit":
                ingredients_list += f"- {quantity} {ing['name']}\n"
            else:
                ingredients_list += f"- {quantity} {ing['unit']} {ing['name']}\n"
        st.markdown(ingredients_list)

        st.markdown(
            "<div class='section-header'>📝 Instructions</div>", unsafe_allow_html=True
        )
        steps_list = ""
        for step in recipe["steps"]:
            # Each step is a dictionary with 'number' and 'description' fields
            if step["description"].strip():  # Only show non-empty steps
                description = capitalize_first_letter(step["description"].strip())
                steps_list += f"{step['number']}. {description}\n"
        st.markdown(steps_list)


def add_social_links():
    """Add social media links in one row, right-aligned"""
    # Adjusted column ratios to bring icons closer together and give more space to the button
    col1, col2, col3, col4, col5 = st.columns([6, 2, 0.6, 0.6, 0.6])

    # Buy Me a Coffee button
    with col2:
        st.markdown(
            """
            <div style="display: flex; justify-content: flex-end;">
                <a href="https://www.buymeacoffee.com/vianmixt" target="_blank">
                    <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" 
                         alt="Buy Me A Coffee" 
                         style="height: 38px; width: auto; min-width: 160px; max-width: 100%;">
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # GitHub icon
    with col3:
        st.markdown(
            """
            <div style="display: flex; justify-content: center;">
                <a href="https://github.com/VianneyMI/baker" target="_blank">
                    <img src="https://cdn.jsdelivr.net/npm/simple-icons@v8/icons/github.svg" 
                         alt="GitHub"
                         style="height: 24px; filter: invert(30%);">
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Medium icon
    with col4:
        st.markdown(
            """
            <div style="display: flex; justify-content: center;">
                <a href="https://medium.com/@vianney.mixtur_39698" target="_blank">
                    <img src="https://cdn.jsdelivr.net/npm/simple-icons@v8/icons/medium.svg" 
                         alt="Medium"
                         style="height: 24px; filter: invert(30%);">
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # LinkedIn icon
    with col5:
        st.markdown(
            """
            <div style="display: flex; justify-content: center;">
                <a href="https://linkedin.com/in/vianney-mixtur-pro/" target="_blank">
                    <img src="https://cdn.jsdelivr.net/npm/simple-icons@v8/icons/linkedin.svg" 
                         alt="LinkedIn"
                         style="height: 24px; filter: invert(30%);">
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )


def add_sidebar_content():
    """Add sidebar content"""
    st.sidebar.markdown(
        """
        ---
        Made with ❤️ using Streamlit
        """
    )


def set_page_config():
    """Configure the Streamlit page"""
    st.set_page_config(
        page_title="Baker",
        page_icon="🥘",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def add_custom_css():
    """Add custom CSS to improve the look and feel"""
    st.markdown(
        """
        <style>
        /* Main title styling */
        .main-title {
            text-align: center;
            color: #2c3e50;
            padding: 1rem 0;
            margin-bottom: 2rem;
        }
        
        /* Recipe title styling */
        .recipe-title {
            color: #2c3e50;
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }
        
        /* Section headers */
        .section-header {
            color: #34495e;
            font-size: 1.2rem;
            margin: 1rem 0;
        }
        
        /* Form styling */
        .stForm {
            background-color: #f8f9fa;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Input field labels */
        .stTextInput label, .stNumberInput label, .stSelectbox label {
            color: #34495e;
            font-weight: 500;
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            background-color: #f8f9fa;
            border-radius: 5px;
        }
        
        /* Success message styling */
        .success-message {
            padding: 1rem;
            border-radius: 5px;
            background-color: #d4edda;
            color: #155724;
            margin: 1rem 0;
        }
        
        /* Warning message styling */
        .warning-message {
            padding: 1rem;
            border-radius: 5px;
            background-color: #fff3cd;
            color: #856404;
            margin: 1rem 0;
        }
        
        /* Social links hover effect */
        .social-links a:hover img {
            filter: invert(50%) !important;
        }
        
        /* Container for proper positioning */
        .main-container {
            position: relative;
            padding-top: 3rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main():
    set_page_config()
    add_custom_css()

    # Title with custom styling
    st.markdown(
        "<h1 class='main-title'>🥘 Baker: The Recipe Finder</h1>",
        unsafe_allow_html=True,
    )

    # Add social links after the title
    add_social_links()

    # Add vertical space
    st.markdown("<div style='margin: 2.5rem 0;'></div>", unsafe_allow_html=True)

    # Add description with increased font size
    st.markdown(
        """
        <div style='text-align: center; margin-bottom: 2rem; font-size: 1.15em;'>
        Find delicious recipes based on the ingredients you have at hand.
        Simply enter your ingredients and desired serving size below.
        </div>
        """,
        unsafe_allow_html=True,
    )

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
                with st.spinner("🔍 Searching for recipes..."):
                    recipes = call_recipes_api(ingredients, serving_size)

                if recipes:
                    st.markdown(
                        f"<div class='success-message'>✨ Found {len(recipes)} recipes!</div>",
                        unsafe_allow_html=True,
                    )
                    for recipe in recipes:
                        display_recipe(recipe)
                else:
                    st.markdown(
                        "<div class='warning-message'>😕 No recipes found with these ingredients.</div>",
                        unsafe_allow_html=True,
                    )


if __name__ == "__main__":
    main()
