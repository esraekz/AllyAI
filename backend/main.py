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

# Create an endpoint to suggest restaurants using OpenAI's new completions API
@app.post("/suggest_restaurant")
async def suggest_restaurant(query: RestaurantQuery):
    try:
        # Use the correct API call for OpenAI>=1.0.0
        response = openai.completions.create(
            model="gpt-3.5-turbo",  # You can use "gpt-4" if available
            prompt=f"Suggest some restaurants based on the query: {query.query}",
            max_tokens=50
        )

        # Extract suggestions from OpenAI response
        suggestions = response['choices'][0]['text'].strip().split("\n")
        return {"query": query.query, "suggestions": suggestions}
    
    except Exception as e:
        return {"error": str(e)}

# Root endpoint for checking FastAPI
@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}
