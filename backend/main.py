from fastapi import FastAPI
from pydantic import BaseModel
import os
from fastapi.middleware.cors import CORSMiddleware
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate  # Updated import for PromptTemplate
from langchain_community.llms import OpenAI as LangchainOpenAI  # Import from langchain_community

# Set OpenAI API key from environment variables (handled by Render or other deployment environment)
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("OpenAI API key not found in environment variables")

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
        
        # Use Langchain's OpenAI LLM wrapper from langchain_community
        llm = LangchainOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)
        
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
