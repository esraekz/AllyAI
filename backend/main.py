from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
from fastapi.middleware.cors import CORSMiddleware

# Set OpenAI API key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; replace with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the model for the restaurant query
class RestaurantQuery(BaseModel):
    query: str

# Create an endpoint to suggest restaurants using OpenAI's ChatCompletion API
@app.post("/suggest_restaurant")
async def suggest_restaurant(query: RestaurantQuery):
    try:
        # Call OpenAI API to get restaurant suggestions using the ChatCompletion endpoint
        response = openai.chat.completion.create(
            model="gpt-3.5-turbo",  # or gpt-4 if available
            messages=[{"role": "user", "content": f"Suggest some restaurants based on the query: {query.query}"}],
            max_tokens=50
        )

        # Extract the assistant's message from the response
        suggestions_text = response['choices'][0]['message']['content']

        # You can split the suggestions by commas or new lines if needed, depending on how they are returned
        suggestions = suggestions_text.strip().split(',')  # Adjust this depending on the format

        return {"query": query.query, "suggestions": suggestions}
    
    except Exception as e:
        return {"error": str(e)}

# Root endpoint for checking FastAPI
@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}
