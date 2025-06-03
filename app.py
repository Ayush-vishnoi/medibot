from flask import Flask, render_template, request, jsonify
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_community.llms import Together
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import system_prompt
import os
import re

def trim_response_to_sentences(text, max_sentences=3):
    sentences = re.split(r'(?<=[.!?]) +', text.strip())
    return ' '.join(sentences[:max_sentences])


os.environ["TOKENIZERS_PARALLELISM"] = "false"


app=Flask(__name__)
load_dotenv()

PINECONE_API_KEY=os.environ.get("PINECONE_API_KEY")
TOGETHER_API_KEY=os.environ.get("TOGETHER_API_KEY")

os.environ['PINECONE_API_KEY']=PINECONE_API_KEY
os.environ['TOGETHER_API_KEY']=TOGETHER_API_KEY

embeddings=download_hugging_face_embeddings()

index_name="medibot"

docsearch=PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever=docsearch.as_retriever(search_type="similarity",search_kwargs={"k":1})


llm = Together(model="mistralai/Mistral-7B-Instruct-v0.1",temperature=0.5,
    max_tokens=512,)


prompt=ChatPromptTemplate.from_messages(
    [
    ("system",system_prompt),
    ("human","{input}"),
    ]
)


question_answer_chain=create_stuff_documents_chain(llm,prompt)
rag_chain=create_retrieval_chain(retriever,question_answer_chain)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get",methods=["GET","POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    
    
    response = rag_chain.invoke({"input": msg})
    full_answer = response["answer"]
    trimmed = trim_response_to_sentences(full_answer)
    
    print("Response (trimmed):", trimmed)
    return str(trimmed)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=6969,debug=True)
