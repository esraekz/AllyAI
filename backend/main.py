from fastapi import FastAPI
from pydantic import BaseModel
import os
from fastapi.middleware.cors import CORSMiddleware
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI  # Correct import for ChatOpenAI
from langchain.chains import LLMChain

# Ensure OpenAI API key is set from environment variables
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

# Create an endpoint to suggest restaurants using Langchain with ChatOpenAI
@app.post("/suggest_restaurant")
async def suggest_restaurant(query: RestaurantQuery):
    try:
        # Define a prompt template using Langchain
        prompt_template = PromptTemplate(
            template="Suggest some restaurants based on the following query: {query}",
            input_variables=["query"]
        )
        
        # Use ChatOpenAI instead of LangchainOpenAI
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)
        
        # Create an LLMChain to link the prompt template and the language model
        chain = LLMChain(prompt=prompt_template, llm=llm)
        
        # Run the chain with the user's query
        response = chain.run(query.query)
        
        # Extract suggestions from the Langchain response
        suggestions = response.strip().split("\n")
        
        return {"query": query.query, "suggestions": suggestions}
    
    except Exception as e:
        return {"error": str(e)}

# Root endpoint for checking FastAPI
@app.get("/")
async def root():
    return {"message": "Hello, FastAPI with Langchain!"}
