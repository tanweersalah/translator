from fastapi import FastAPI
import os
from dotenv import load_dotenv
import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langserve import add_routes

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY") 
os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")
os.environ['LANGCHAIN_PROJECT'] = os.getenv("LANGCHAIN_PROJECT")



#groq_api_key = st.secrets["GROQ_API_KEY"]
#os.environ['LANGCHAIN_API_KEY'] = st.secrets["LANGCHAIN_API_KEY"]
#os.environ['LANGCHAIN_PROJECT'] = st.secrets["LANGCHAIN_PROJECT"]

os.environ['LANGCHAIN_TRACING_V2'] = "true"

model = ChatGroq(model="llama3-70b-8192")




parser = StrOutputParser()



prompt = ChatPromptTemplate.from_messages({
    ("system","Translate the following sentences from {source_language} to {target_language}" ),
    ("human", "{input}")
    })

chain = prompt|model|parser



## App defination

app = FastAPI(title="Langauge Translator", version="1", description="API Server using langchain")

add_routes(
    app,
    chain,
    path="/chain"
)

import uvicorn

if __name__ == "__main__":
    uvicorn.run(app,host="localhost", port=8080)
