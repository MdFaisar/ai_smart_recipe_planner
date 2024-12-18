# src/cuisine_fusion.py

def generate_fusion_recipe(client, user_preferences, recipes):
    prompt = f"""
    Generate a fusion recipe combining elements from two different cuisines:
    Cuisine preferences: {user_preferences['cuisine_preferences']}
    Dietary restrictions: {user_preferences['dietary_restrictions']}
    Skill level: {user_preferences['skill_level']}
    
    Create a unique recipe that blends techniques, ingredients, or flavors from two distinct culinary traditions.
    Format the recipe with a creative title, ingredients list, and step-by-step instructions.
    """
    
    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a creative chef assistant that generates fusion recipes."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.8
    )
    
    return response.choices[0].message.content