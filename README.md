# Architecture
backend/
  app/
    --main.py
    --database.py
    models/
    --users.py
    --company.py
    --job.py
    schemas/
    --users.py
    --company.py
    --job.py
    routers/
    --users.py
    --company.py
    --job.py
    utils/
    --token.py
    --security.py
    --oauth2.py
    --
  alembic.ini
  alembic/env.py


# Task 
1.push to github
2.try run application ./env/Scripts/activate --> uvicorn app.main:app --reload
3.dont blindly trusting on Ai
4.read the error look for our file name dont care of other files errors like library files errors
5.if files doesnt have error if its like unprocessible identifier or dependency error then ask ai to fix it
6.ask ai to suggest changes not to correct-----
register->login->create compnay->create job
have two variants -> role1:admin
role2:candidate-->try test all apis with both roles

flow of full app
react->login->oauthform->accesstoken->store in local->send with every request->logout

react  -> axios->   fastapi_url  ->  token  ->header->  response  ->  store in local browser to remeber the login-> 
then you can call or use the apis you want--> then for all the apis use this axios function to call the apis-> fetchcompany() use axios.get(url) ->fastapi-> postgresql_db ->return response to axios -> store in local state and show in ui

LLM-Large Language Models
Tokenization-sentence into words in list ->like this ["" "",""]

Embeddings-sentence into vector numbers -> like this [1,2,3,4,5]

Transformer-it do the prediction of next word on basis of previous words embeddings

transformer -> self atention mechanism->it is used to give the weights to the words in the sentence


SSE-Server sent events ->it is used to send the response from server to client in form of chunks of text so that we can show the response in form of chunks of text like chatbot ui

RAG-Retrieval Augmented Generation-it is used to increase the accuracy of llm by providing relevant information to the llm

context-window-it is the maximum number of words that the llm can process at a time

Langchain->it's a framework to build llms ,its useful to connect llm to external sources of information->like database,files,websites
->it is used to create complex workflows of llm->like chatbot that can answer questions about specific documents

POSTGRES_URL="postgres://postgres.hpbxffhiewpvfiakaewn:yxLAul0U1Xy1p4l8@aws-1-ap-south-1.pooler.supabase.com:6543/postgres?sslmode=require&supa=base-pooler.x"

POSTGRES_HOST=aws-1-ap-south-1.pooler.supabase.com
POSTGRES_PORT=6543
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yxLAul0U1Xy1p4l8
POSTGRES_DB=postgres

RAG->Retrieval Augmented Generation
It is used to increase the accuracy of llm by providing relevant information to the llm->it is used to increase the accuracy of llm by providing relevant information to the llm

How it will make chunks in vector db?
let's say we have 3 documents->one each one has 100 words
so it will make 3 chunks--each chunk will overlap with previous chunk by 100 chars->so each chunk will have 500 chars
like 0-499
400-899
800-1399

this chunk will be converted into vectors
eg:i am a python developer. i have 3 years of experience in python development.
i have good knowledge of python development and i am a good python developer.
i have good knowledge of fastapi
->will convert all the 3 chunks into vectors

goldilocks principle->just right amount of information
semantic search->it is used to find the most relevant information to the query->it is used to find the most relevant information to the query

semantic similarity
it is used to find the most similar vectors
if two vectors are close to each other then they are similar

cosine similarity->used in nlp to find the similarity between two vectors

qdrantdb is vector database
it is used to store the vectors and do the semantic search

embeddings model->it is used to convert the text into vectors

initially without rag 
user query->send to llm->here transformers model will answer based on its training data->response

with rag
user query->embed done by embeddings model->vector->semantic search done by qdrantdb(vector db)->retrieve relevant chunks->construct prompt->combined text + query->
->llm->response

