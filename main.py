# from fastapi import FastAPI
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# origins = ["*"]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class QueryData(BaseModel):
#     knowledge_text: str
#     question_text: str

# @app.post("/api/ask")
# def ask_question(query: QueryData):
#     knowledge_base = query.knowledge_text
#     question = query.question_text.lower()
    
#     stop_words = {'is', 'a', 'the', 'what', 'are', 'in', 'for', 'of', 'to', 'do'}
#     query_words = set(word for word in question.split() if word not in stop_words and len(word) > 2)

#     best_sentence = "Sorry, I could not find a relevant answer in the provided text."
#     max_score = 0

#     for sentence in knowledge_base.split('.'):
#         if not sentence:
#             continue
        
#         current_score = 0
#         sentence_words = set(sentence.lower().split())

#         for word in query_words:
#             if word in sentence_words:
#                 current_score += 1
        
#         if current_score > max_score:
#             max_score = current_score
#             best_sentence = sentence.strip()

#     if max_score == 0:
#         return {"answer": "Sorry, I could not find a relevant answer for your question."}
    
#     return {"answer": best_sentence}

# @app.get("/")
# def read_root():
#     return {"Status": "Dynamic KnowledgeScout API is running!"}


import string  # Import the string library to handle punctuation
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryData(BaseModel):
    knowledge_text: str
    question_text: str

@app.post("/api/ask")
def ask_question(query: QueryData):
    knowledge_base = query.knowledge_text
    question = query.question_text.lower()
    
    stop_words = {'is', 'a', 'the', 'what', 'are', 'in', 'for', 'of', 'to', 'do'}
    
    # FINAL FIX: This line now removes all punctuation (like ?, !, .) from the question words
    query_words = set(
        word.strip(string.punctuation) for word in question.split() 
        if word.strip(string.punctuation) not in stop_words and len(word.strip(string.punctuation)) > 2
    )

    best_sentence = "Sorry, I could not find a relevant answer in the provided text."
    max_score = 0

    for sentence in knowledge_base.split('.'):
        if not sentence:
            continue
        
        current_score = 0
        
        # FINAL FIX: This line also removes punctuation from the knowledge base words before comparing
        sentence_words = set(word.strip(string.punctuation) for word in sentence.lower().split())

        for word in query_words:
            if word in sentence_words:
                current_score += 1
        
        if current_score > max_score:
            max_score = current_score
            best_sentence = sentence.strip()

    if max_score == 0:
        return {"answer": "Sorry, I could not find a relevant answer for your question."}
    
    return {"answer": best_sentence}

@app.get("/")
def read_root():
    return {"Status": "Dynamic KnowledgeScout API is running!"}
