# src/recipe_generator.py

def generate_recipe(client, user_preferences, recipes, seasonal_ingredients):
    prompt = f"""
    Generate a recipe based on the following preferences:
    Dietary restrictions: {user_preferences['dietary_restrictions']}
    Cuisine preferences: {user_preferences['cuisine_preferences']}
    Skill level: {user_preferences['skill_level']}
    Available ingredients: {user_preferences['available_ingredients']}
    
    Consider seasonal ingredients: {seasonal_ingredients}
    
    Format the recipe with a title, ingredients list, and step-by-step instructions.
    """
    
    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates recipes."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.7
    )
    
    return response.choices[0].message.content