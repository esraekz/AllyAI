import openai

openai.api_key = "your-openai-api-key"  # Replace with your OpenAI API key

@app.post("/suggest_restaurant")
async def suggest_restaurant(query: RestaurantQuery):
    try:
        # Call OpenAI API for suggestions
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Suggest restaurants based on this preference: {query.query}",
            max_tokens=100,
            temperature=0.7
        )
        
        suggestion = response.choices[0].text.strip()
        return {"query": query.query, "suggestions": suggestion}
    
    except Exception as e:
        return {"error": str(e)}
