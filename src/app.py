import streamlit as st
import groq
import os
import json
from pathlib import Path
import sys

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

# Set up Groq client
groq_api_key = os.environ.get("GROQ_API_KEY")
if not groq_api_key:
    st.error("Please set the GROQ_API_KEY environment variable")
    st.stop()
client = groq.Groq(api_key=groq_api_key)

# Load data
def load_json(filename):
    file_path = project_root / 'data' / filename
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Error: {filename} not found in {file_path}")
        return {}

recipes = load_json('recipes.json')
seasonal_ingredients = load_json('seasonal_ingredients.json')

# Import custom modules
from src.recipe_generator import generate_recipe
from src.meal_planner import create_meal_plan
from src.nutritional_analyzer import analyze_nutrition
from src.cuisine_fusion import generate_fusion_recipe
from src.shopping_list_generator import generate_shopping_list

def format_content(content):
    lines = content.split('\n')
    formatted_lines = []
    for line in lines:
        if line.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
            formatted_lines.append('- ' + line.split('.', 1)[1].strip())
        else:
            formatted_lines.append(line)
    return '\n'.join(formatted_lines)

def main():
    st.set_page_config(page_title="Smart Recipe Planner", page_icon="🍽️", layout="wide")
    
    # Add custom CSS with advanced effects
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    
    :root {
        --primary-color: #3498db;
        --secondary-color: #2c3e50;
        --background-color: #f5f7fa;
        --card-background: #ffffff;
        --text-color: #2c3e50;
        --hover-color: #2980b9;
    }

    .stApp {
        background-color: var(--background-color);
        color: var(--text-color);
        font-family: 'Poppins', sans-serif;
    }

    .stTextInput, .stSelectbox, .stTextArea {
        background-color: var(--card-background);
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        padding: 10px;
        font-size: 16px;
        transition: all 0.3s ease;
    }

    .stTextInput:focus, .stSelectbox:focus, .stTextArea:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
    }

    .stButton>button {
        background-color: var(--primary-color);
        color: white;
        font-weight: 600;
        border-radius: 8px;
        border: none;
        padding: 12px 24px;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background-color: var(--hover-color);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }

    h1, h2, h3 {
        color: var(--secondary-color);
        font-weight: 600;
    }

    .output-container {
        background-color: var(--card-background);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
        transition: all 0.3s ease;
    }

    .output-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
    }

    .output-section {
        margin-bottom: 20px;
        border-bottom: 1px solid #e0e0e0;
        padding-bottom: 20px;
    }

    .output-section:last-child {
        border-bottom: none;
    }

    .navbar {
        padding: 10px 0;
        background-color: var(--secondary-color);
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 999;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }

    .navbar ul {
        list-style-type: none;
        margin: 0;
        padding: 0;
        overflow: hidden;
    }

    .navbar li {
        float: left;
    }

    .navbar li a {
        display: block;
        color: white;
        text-align: center;
        padding: 14px 16px;
        text-decoration: none;
        transition: all 0.3s ease;
    }

    .navbar li a:hover {
        background-color: rgba(255,255,255,0.1);
        transform: translateY(-2px);
    }

    .content {
        margin-top: 60px;
        padding: 20px;
    }

    .about-section {
        background-color: var(--card-background);
        border-radius: 12px;
        padding: 30px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
        transition: all 0.3s ease;
    }

    .about-section:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
    }

    .about-section h2 {
        color: var(--primary-color);
        margin-bottom: 20px;
    }

    .about-section p {
        font-size: 18px;
        line-height: 1.6;
        margin-bottom: 20px;
    }

    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 30px;
        margin-top: 30px;
    }

    .feature-card {
        background-color: var(--card-background);
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .feature-card:hover {
        transform: translateY(-10px) rotateY(10deg);
        box-shadow: 0 12px 20px rgba(0, 0, 0, 0.15);
    }

    .feature-card h3 {
        color: var(--primary-color);
        margin-bottom: 10px;
    }

    .feature-card p {
        font-size: 16px;
    }

    /* Advanced animations and effects */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .fade-in-up {
        animation: fadeInUp 0.6s ease-out;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }

    .float {
        animation: float 3s ease-in-out infinite;
    }

    .hover-zoom {
        transition: transform 0.3s ease;
    }

    .hover-zoom:hover {
        transform: scale(1.05);
    }

    .rotate-on-hover {
        transition: transform 0.5s ease;
    }

    .rotate-on-hover:hover {
        transform: rotate(5deg) scale(1.05);
    }

    .card-3d {
        perspective: 1000px;
        transform-style: preserve-3d;
        transition: transform 0.5s;
    }

    .card-3d:hover {
        transform: rotateY(15deg) scale(1.05);
    }

    @keyframes glow {
        0%, 100% { box-shadow: 0 0 5px var(--primary-color); }
        50% { box-shadow: 0 0 20px var(--primary-color), 0 0 30px var(--primary-color); }
    }

    .glow {
        animation: glow 2s infinite;
    }

    /* Parallax scrolling effect */
    .parallax {
        background-attachment: fixed;
        background-position: center;
        background-repeat: no-repeat;
        background-size: cover;
    }

    /* Gradient text effect */
    .gradient-text {
        background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        display: inline-block;
    }

    /* Stagger animation for list items */
    @keyframes fadeInStagger {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .stagger-animation > * {
        opacity: 0;
        animation: fadeInStagger 0.5s ease-out forwards;
    }

    .stagger-animation > *:nth-child(1) { animation-delay: 0.1s; }
    .stagger-animation > *:nth-child(2) { animation-delay: 0.2s; }
    .stagger-animation > *:nth-child(3) { animation-delay: 0.3s; }
    .stagger-animation > *:nth-child(4) { animation-delay: 0.4s; }
    .stagger-animation > *:nth-child(5) { animation-delay: 0.5s; }

    /* Neon text effect */
    .neon-text {
        color: #fff;
        text-shadow:
            0 0 5px #fff,
            0 0 10px #fff,
            0 0 20px #fff,
            0 0 40px var(--primary-color),
            0 0 80px var(--primary-color),
            0 0 90px var(--primary-color),
            0 0 100px var(--primary-color),
            0 0 150px var(--primary-color);
    }

    /* Animated background gradient */
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .gradient-bg {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }

    </style>
    """, unsafe_allow_html=True)

    # Navbar
    st.markdown("""
    <div class="navbar">
        <ul>
            <li><a href="#home">Home</a></li>
            <li><a href="#about">About</a></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Content
    st.markdown('<div class="content fade-in-up">', unsafe_allow_html=True)

    # Home Section
    st.markdown('<div id="home">', unsafe_allow_html=True)
    st.markdown('<h1 class="gradient-text">🍽️ Smart Recipe Generator and Meal Planner</h1>', unsafe_allow_html=True)

    with st.sidebar:
        st.header("User Preferences")
        dietary_restrictions = st.multiselect("Dietary Restrictions", ["Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free", "Nut-Free", "Low-Carb"])
        cuisine_preferences = st.multiselect("Preferred Cuisines", ["Italian", "Mexican", "Chinese", "Indian", "Japanese", "Mediterranean", "American", "Thai", "French"])
        skill_level = st.select_slider("Cooking Skill Level", options=["Beginner", "Intermediate", "Advanced"])
        available_ingredients = st.text_area("Available Ingredients (comma-separated)")

    user_preferences = {
        "dietary_restrictions": dietary_restrictions,
        "cuisine_preferences": cuisine_preferences,
        "skill_level": skill_level.lower(),
        "available_ingredients": [ing.strip() for ing in available_ingredients.split(',') if ing.strip()],
    }

    if st.button("Generate Meal Plan", key="generate_button"):
        with st.spinner("Cooking up your personalized meal plan..."):
            recipe = generate_recipe(client, user_preferences, recipes, seasonal_ingredients)
            meal_plan = create_meal_plan(client, user_preferences, recipes, seasonal_ingredients)
            nutrition_analysis = analyze_nutrition(client, meal_plan)
            fusion_recipe = generate_fusion_recipe(client, user_preferences, recipes)
            shopping_list = generate_shopping_list(client, meal_plan)

        st.success("Your personalized meal plan is ready!")

        col1, col2 = st.columns(2)

        with col1:
            with st.expander("📝 Generated Recipe", expanded=True):
                st.markdown('<div class="card-3d output-container">', unsafe_allow_html=True)
                st.markdown('<div class="stagger-animation">', unsafe_allow_html=True)
                st.markdown(format_content(recipe))
                st.markdown('</div></div>', unsafe_allow_html=True)

            with st.expander("🍽️ Weekly Meal Plan", expanded=True):
                st.markdown('<div class="hover-zoom output-container">', unsafe_allow_html=True)
                st.markdown('<div class="stagger-animation">', unsafe_allow_html=True)
                st.markdown(format_content(meal_plan))
                st.markdown('</div></div>', unsafe_allow_html=True)

        with col2:
            with st.expander("🥗 Nutritional Analysis", expanded=True):
                st.markdown('<div class="rotate-on-hover output-container">', unsafe_allow_html=True)
                st.markdown(format_content(nutrition_analysis))
                st.markdown('</div></div>', unsafe_allow_html=True)

            with st.expander("🌶️ Fusion Recipes", expanded=True):
                st.markdown('<div class="card-3d output-container">', unsafe_allow_html=True)
                st.markdown('<div class="stagger-animation">', unsafe_allow_html=True)
                st.markdown(format_content(fusion_recipe))
                st.markdown('</div></div>', unsafe_allow_html=True)

            with st.expander("🛒 Smart Shopping Lists", expanded=True):
                st.markdown('<div class="hover-zoom output-container">', unsafe_allow_html=True)
                st.markdown('<div class="stagger-animation">', unsafe_allow_html=True)
                st.markdown(format_content(shopping_list))
                st.markdown('</div></div>', unsafe_allow_html=True)

    # Add Feature Cards for Fusion Recipes, Smart Shopping Lists, and Seasonal Ingredients
    st.markdown('<div class="feature-grid">', unsafe_allow_html=True)
    features = [
        ("🌶️ Fusion Recipes", "Explore exciting culinary fusions from different cuisines."),
        ("🛒 Smart Shopping Lists", "Generate comprehensive shopping lists for your meal plans."),
        ("🌿 Seasonal Ingredients", "Discover and use fresh, seasonal ingredients in your cooking.")
    ]
    for title, description in features:
        st.markdown(f"""
        <div class="feature-card hover-zoom">
            <h3>{title}</h3>
            <p>{description}</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()