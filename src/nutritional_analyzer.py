def analyze_nutrition(client, meal_plan):
    prompt = f"""
    Analyze the nutritional content of the following meal plan:
    {meal_plan}
    
    Provide detailed nutritional breakdown, including:
    - Calories
    - Macronutrient distribution (carbs, proteins, fats)
    - Micronutrient levels
    - Suggestions for improving nutritional balance
    """

    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that analyzes nutritional content of meal plans."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.3
    )

    return response.choices[0].message.content
