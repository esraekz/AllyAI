from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the model for the restaurant query
class RestaurantQuery(BaseModel):
    query: str

# Create an endpoint to suggest restaurants using OpenAI
@app.post("/suggest_restaurant")
async def suggest_restaurant(query: RestaurantQuery):
    try:
        # Call OpenAI API to get restaurant suggestions
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Suggest some restaurants based on the query: {query.query}",
            max_tokens=50
        )

        # Extract suggestions from OpenAI response
        suggestions = response['choices'][0]['text'].strip().split("\n")
        return {"query": query.query, "suggestions": suggestions}
    
    except Exception as e:
        return {"error": str(e)}

# A simple root endpoint to check if FastAPI is running
@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}
