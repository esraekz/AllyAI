from fastapi import FastAPI
from pydantic import BaseModel
import os
from fastapi.middleware.cors import CORSMiddleware
from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenAI
from dotenv import load_dotenv

#load_dotenv()  # Ensure environment variables from .env file are loaded
# Set OpenAI API key from environment variables (handled by Render or other deployment environment)
openai.api_key = os.getenv('OPENAI_API_KEY')

print(f"OpenAI API Key: {os.getenv('OPENAI_API_KEY')}")

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

# Create an endpoint to suggest restaurants using Langchain with OpenAI
@app.post("/suggest_restaurant")
async def suggest_restaurant(query: RestaurantQuery):
    try:
        # Define a prompt template using Langchain
        prompt_template = PromptTemplate(
            template="Suggest some restaurants based on the following query: {query}",
            input_variables=["query"]
        )
        
        # Use Langchain's OpenAI LLM wrapper
        llm = OpenAI(model_name="gpt-3.5-turbo")  # Use "gpt-4" if available
        
        # Create an LLMChain to link the prompt template and the language model
        chain = LLMChain(prompt=prompt_template, llm=llm)
        
        # Run the chain with the user's query
        response = chain.run(query.query)
        
        # Extract suggestions from Langchain response
        suggestions = response.strip().split("\n")
        
        return {"query": query.query, "suggestions": suggestions}
    
    except Exception as e:
        return {"error": str(e)}

# Root endpoint for checking FastAPI
@app.get("/")
async def root():
    return {"message": "Hello, FastAPI with Langchain!"}
