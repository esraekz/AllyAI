from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()


# Define the model for the restaurant query
class RestaurantQuery(BaseModel):
    query: str

# Create an endpoint to suggest restaurants
@app.post("/suggest_restaurant")
async def suggest_restaurant(query: RestaurantQuery):
    sample_suggestions = ["Sushi Place", "Pizza Corner", "Taco Town"]
    return {"query": query.query, "suggestions": sample_suggestions}
