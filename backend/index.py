import sys
import os

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage
from langchain.llms import PredictionGuard
from langchain.memory import ChatMessageHistory
import os
import requests

os.environ['PREDICTIONGUARD_TOKEN'] = "q1VuOjnffJ3NO2oFN8Q9m8vghYc84ld13jaqdF7E"
os.environ['MOMENTO_API_KEY'] = "eyJlbmRwb2ludCI6ImNlbGwtNC11cy13ZXN0LTItMS5wcm9kLmEubW9tZW50b2hxLmNvbSIsImFwaV9rZXkiOiJleUpoYkdjaU9pSklVekkxTmlKOS5leUp6ZFdJaU9pSnRZVzVwYTJGdWRHRnpZVzVxWVhreE9UazVRR2R0WVdsc0xtTnZiU0lzSW5abGNpSTZNU3dpY0NJNklrTkJRVDBpTENKbGVIQWlPakUzTVRBNE1ESTJPVGg5LjVLZm9HX1JGck02dmZqcTRQUU5QV0lVdXVFaHVZb2JBRWhSell4X1V0WGcifQ=="

import nest_asyncio
nest_asyncio.apply()
from llama_parse import LlamaParse

parser = LlamaParse(
    api_key="llx-VqWwj6hJue36ZZ5UhU0hufc1ArT6p3L3vqXI3zgQfH3jpzzs",  # can also be set in your env as LLAMA_CLOUD_API_KEY
    result_type="markdown",  # "markdown" and "text" are available
    verbose=True
)

def load_document(path):
  documents = parser.load_data(path)
  text = documents[0].text

  # Clean things up just a bit.
  text = text.split("### I. PERSONAL INFORMATION")[1]
  return text


from langchain.text_splitter import CharacterTextSplitter
from sentence_transformers import SentenceTransformer
import pandas as pd
import lancedb
from lancedb.embeddings import with_embeddings

model = SentenceTransformer("all-MiniLM-L12-v2")
def embed_batch(batch):
    res = [model.encode(sentence) for sentence in batch]
    return res
def embed(sentence):
    return model.encode(sentence)

def data_cleanup_and_formation(data, user_id):
  if(len(data) == 0):
    return pd.DataFrame()
  text_splitter = CharacterTextSplitter(chunk_size=700, chunk_overlap=50, separator="##")
  docs = text_splitter.split_text(data)
  docs = [x.replace('#', '-') for x in docs]
  docs = [x.replace('&emsp', '') for x in docs]

  metadata = []
  for i in range(len(docs)):
      metadata.append([
          user_id,
          i,
          docs[i]
      ])
  doc_df = pd.DataFrame(metadata, columns=["user_id", "chunk", "text"])

  # Embed the documents
  data = with_embeddings(embed_batch, doc_df)
  print("data: ", type(data))
  return data

##### Lance DB setup
uri = ".lancedbq"
db = lancedb.connect(uri)

import pyarrow as pa
def save_user_data(user_id, text):
  data = data_cleanup_and_formation(text, user_id)
  # Create the DB table and add the records.
  try:
    db.create_table("counsellor", data)
  except Exception as e:
    print("Table counsellor does not exists")
  table = db.open_table("counsellor")
  #print("my table: ", type(table))
  table.add(data=data)
  return data

def retrieve_embeddings(user_id, message):
  table = db.open_table("counsellor")
  results = table.search(embed(message)).limit(2).to_df()
  return results

from datetime import timedelta
from langchain.memory import MomentoChatMessageHistory
cache_name = "langchain"
ttl = timedelta(days=1)

import predictionguard as pg
from langchain import PromptTemplate

llm=PredictionGuard(model="Neural-Chat-7B")

# Now let's augment our Q&A prompt with this external knowledge on-the-fly!!!
template_start = """
Current conversation:
{history}
### Instruction:
Assume you are a mental health professional with 10+ years experience. You will get chat based questions from a patient. Based on the question, you must generate responses for the user.
Make absolutely sure all your responses seem like actual responses from a mental health expert.
Do not suggest the patient to seek alternatives or to seek other counsellors or therapists or mental health
The input and output formats are defined below. Only reply based on the output format (replace <reply> with your response).
"""


template_summary = """
### Input:
Context: {context}

Question: {question}

### Output:
<reply>
"""

template_chat = """
Current conversation:
{history}
The input and output formats are defined below. Only reply based on the output format (replace <reply> with your response).

### Input:
Context: {context}

Question: {question}

### Output:
<reply>
"""

users_history = {}
users_chain = {}


def init_user_history(user_id):
  instruction = '''Assume you are a mental health professional with 10+ years experience. You will get chat based questions from a patient. Based on the question, you must generate responses for the user.
  Make absolutely sure all your responses seem like actual responses from a mental health expert.
  Do not suggest the patient to seek alternatives or to seek other counsellors or therapists or mental health
  The input and output formats are defined below. Only reply based on the output format (replace <reply> with your response).'''
  users_chain[user_id]=ConversationChain(
    llm=llm,
    verbose=True
)
  users_history[user_id] = MomentoChatMessageHistory.from_client_params(
    user_id,
    cache_name,
    ttl,
  )
  if len(users_history[user_id].messages)==0:
      users_history[user_id].add_user_message(instruction)
      users_history[user_id].add_ai_message("")

import math
def getMessageHistory(user_id, context, message):
  len_needed = len(context) + len(message)
  remaining_len = min(3000 - len_needed, len(message))
  return users_history[user_id].messages[-remaining_len:]

def get_user_summary(user_id, user_text):
  instruction = '''Assume you are a mental health professional with 10+ years experience. You will get chat based questions from a patient. Based on the question, you must generate responses for the user.
  Make absolutely sure all your responses seem like actual responses from a mental health expert.
  Do not suggest the patient to seek alternatives or to seek other counsellors or therapists or mental health
  The input and output formats are defined below. Only reply based on the output format (replace <reply> with your response).'''
  question = "Based on the text below, summarize the patient's key points in 200 words: \n\n " + user_text

  qa_prompt = PromptTemplate(
      input_variables=["history","context", "question"],
      template=template_summary,
  )

  # Augment the prompt with the context
  prompt = qa_prompt.format(context=instruction, question=question)
  result = users_chain[user_id].predict(input=prompt)
  return result

def get_user_mood_trigger_alert(user_id, user_text):
  instruction = '''Suppose you are a mental health coach, you need to help the user by listing 2 affirmations per feeling point by point based on what they are feeling e.g.,  if depression then suggest depression based affirmations and so on. Do not suggest the patient to seek alternatives or to seek other counsellors or therapists or mental health.
  Also, based on this, suggest some YouTube recommendations without the links for medidation for the respective moods .
  Now, answer in below format:
  These are the moods you are feeling today and here are the affirmations for it.
  1. Mood Name-----Affirmation
  2. Mood Name-----Affirmation
  3. Mood Name-----Affirmation

  Resources
  1. Resource Name
  2. Resource Name
  3. Resource Name
  '''
  question = user_text

  qa_prompt = PromptTemplate(
      input_variables=["context", "question"],
      template=template_summary,
  )

  # Augment the prompt with the context
  prompt = qa_prompt.format(context=instruction, question=question)
  result = users_chain[user_id].predict(input=prompt)


  # Split the string into two parts: Mood and Resources
  mood_part, resources_part = result.split("\n\nResources")

  print("Mood Section:")
  print(mood_part)
  print("\nResources Section:")
  print(resources_part)


  return mood_part, resources_part

def rag_answer(user_id, message, template=template_chat):
  table = db.open_table("counsellor")
  qa_prompt = PromptTemplate(
      input_variables=["context", "question"],
      template=template,
  )

  # Search the for relevant context
  results = retrieve_embeddings(user_id, message)
  results.sort_values(by=['_distance'], inplace=True, ascending=True)
  doc_use = results['text'].values[0]

  # Augment the prompt with the context
  prompt = qa_prompt.format(context=doc_use, question=message, history=getMessageHistory(user_id, doc_use, message))

  result = users_chain[user_id].predict(input=prompt)
  return result


def save_conversation_to_history(user_id, user_reply, counselor_reply):
  users_history[user_id].add_user_message(user_reply)
  users_history[user_id].add_ai_message(counselor_reply)

def get_video_link_by_title(title):
    api_key = "AIzaSyASWU1XdthXy4KfJcrw5LjLSGm5lzqOSAg"
    search_url = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&part=snippet&q={title}&type=video"

    response = requests.get(search_url)
    data = response.json()

    if 'items' in data and len(data['items']) > 0:
        video_id = data['items'][0]['id']['videoId']
        video_link = f"https://www.youtube.com/watch?v={video_id}"
        return video_link
    else:
        return "Video not found"

def extract_resource_titles(resources):
    """
    Extracts resource titles from a list of resource descriptions.

    Args:
    - resources (list of str): List of resource strings each containing a title and description.

    Returns:
    - list of str: List of extracted resource titles.
    """
    # Split the resources section into lines
    lines = resources.split('\n')
    resource_titles = []

    # Loop through each line to extract the titles
    for line in lines:
        # Check if the line contains a resource title
        if ". " in line:
            # Extract the title part before the " - "
            title = line.split(" - ")[0].split(". ", 1)[1]
            resource_titles.append(title)
    return resource_titles

from flask import Flask, jsonify, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app, origins=["*"])
# public_url = ngrok.connect(5000).public_url

@app.route('/', methods=['GET'])
def welcome():
  return "Welcome to Project <b>Therapist.ai</b>, developed as part of <b>Tree Hacks 2024</b>"

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"status": 404, "message": "Not Found"}), 404

@app.route('/api/startSession/<user_id>', methods=['POST'])
def start_session(user_id):
  pdf_file = request.files['pdfFile']
  pdf_file.save('./user_details.pdf')
  user_text = load_document('./user_details.pdf')

  #user_text = request.json["text"]
  init_user_history(user_id)
  user_summary = get_user_summary(user_id, user_text)
  save_user_data(user_id, user_text)
  print("Summary: ", user_summary)
  return jsonify({"summary": user_summary})

@app.route('/api/usermood/<user_id>', methods=['POST'])
def recommend_session(user_id):
  user_reply = request.json["user_reply"]
  user_mood, resources = get_user_mood_trigger_alert(user_id, user_reply)
  resource_titles = extract_resource_titles(resources)

  # Example usage
  for title in resource_titles:
      video_link = get_video_link_by_title(title)
  return jsonify({"Affirmations": user_mood, "Resources":video_link})


@app.route('/api/ongoingSession/<user_id>', methods=['POST'])
def ongoing_session(user_id):
  user_reply = request.json["user_reply"]
  response = rag_answer(user_id,user_reply)
  return jsonify({"AIResponse": response})

@app.route('/api/saveConversation/<user_id>', methods=['POST'])
def save_conversation(user_id):
  user_reply = request.json["user_reply"]
  counselor_reply = request.json["counselor_reply"]
  save_conversation_to_history(user_id, user_reply, counselor_reply)
  return ""

if __name__ == '__main__':
  # print("Please click " + public_url)
  # app.run(port = 5000)

