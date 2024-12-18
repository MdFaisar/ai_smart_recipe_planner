# src/meal_planner.py

def create_meal_plan(client, user_preferences, recipes, seasonal_ingredients):
    prompt = f"""
    Create a weekly meal plan based on the following preferences:
    Dietary restrictions: {user_preferences['dietary_restrictions']}
    Cuisine preferences: {user_preferences['cuisine_preferences']}
    Skill level: {user_preferences['skill_level']}
    Available ingredients: {user_preferences['available_ingredients']}
    
    Consider seasonal ingredients: {seasonal_ingredients}
    
    Format the meal plan with breakfast, lunch, and dinner for each day of the week.
    """
    
    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that creates meal plans."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        temperature=0.7
    )
    
    return response.choices[0].message.content