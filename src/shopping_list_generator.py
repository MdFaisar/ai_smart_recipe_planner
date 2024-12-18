# src/shopping_list_generator.py

def generate_shopping_list(client, meal_plan):
    prompt = f"""
    Generate a smart shopping list based on the following meal plan:
    {meal_plan}
    
    Create an optimized list that:
    - Combines similar ingredients
    - Suggests appropriate package sizes
    - Considers potential leftovers
    - Groups items by store section (produce, dairy, etc.)
    
    Format the list in a clear, easy-to-read manner.
    """
    
    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates smart shopping lists."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=800,
        temperature=0.5
    )
    
    return response.choices[0].message.content