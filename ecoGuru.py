import pandas as pd
import os
from tqdm.auto import tqdm  # this is our progress bar
import openai
#import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#Data imports
import pandas as pd
import numpy as np
#Pinecone imports
import pinecone
from pinecone import PodSpec
from pinecone import Pinecone
from pinecone import ServerlessSpec
#OpenAI

#openai.api_key = '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'   -- 3.5 Key
from pinecone import Pinecone
import PyPDF2
import openai

openai.api_key = "sk-proj-GLxozGg6qxjAtiaF8wVhT3BlbkFJcBnO9U6FW9frcpQ8Wl0a"   #4 Key

def getData(tokens, overlap, path):

  def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

  # Replace "your_pdf_file.pdf" with the actual file name you uploaded
  pdf_path = path
  text = extract_text_from_pdf(pdf_path)

  def split_text_into_chunks(text, word, overlap):
    # Split the text into a list of words
    words = text.split()
    # Calculate the number of words in each chunk and the number of chunks
    chunk_size = int(word)
    num_chunks = int(len(words) / chunk_size) + 1
    # Calculate the number of overlapping words
    overlap_size = int(chunk_size * overlap)
    # Create a list to store the chunks
    chunks = []
    # Loop through the text and create the chunks
    for i in range(num_chunks):
        # Calculate the start and end indices for the current chunk
        start = i * chunk_size
        end = min((i + 1) * chunk_size, len(words))
        # If this is not the first chunk, add the overlapping words from the previous chunk
        if i > 0:
            start -= overlap_size
        # Create the chunk and add it to the list
        chunk = ' '.join(words[start:end])
        chunks.append(chunk)
    return chunks

  tokens = tokens
  word = tokens * 0.75 #Constant proportion
  overlap = overlap #Number between 0-1 as a percent
  chunks = split_text_into_chunks(text, word, overlap)
  i = 0
  my_list = []
  for chunk in chunks:
      my_list.append(chunk)
  return my_list, extract_text_from_pdf(pdf_path)

def getIndex():
  pc = Pinecone(api_key="d403ddc4-dc54-47d5-9c8f-ed19848d06ce")
  index = pc.Index("quickstart")
  return index

def upserts(q, values, index):
  index = index
  my_list = values

  query = q
  MODEL = "text-embedding-3-small"

  res = openai.Embedding.create(
      input=[query], engine=MODEL
  )

  embeds = [record['embedding'] for record in res['data']]

  # load the first 1K rows of the TREC dataset
  #trec = load_dataset('trec', split='train[:1000]')

  batch_size = 32  # process everything in batches of 32
  for i in tqdm(range(0, len(my_list), batch_size)):
      # set end position of batch
      i_end = min(i+batch_size, len(my_list))
      # get batch of lines and IDs
      lines_batch = my_list[i: i+batch_size]
      ids_batch = [str(n) for n in range(i, i_end)]
      # create embeddings
      res = openai.Embedding.create(input=lines_batch, engine=MODEL)
      embeds = [record['embedding'] for record in res['data']]
      # prep metadata and upsert batch
      meta = [{'text': line} for line in lines_batch]
      to_upsert = zip(ids_batch, embeds, meta)
      # upsert to Pinecone
      index.upsert(vectors=list(to_upsert))

def getRes(query, index):
  query = query
  MODEL = "text-embedding-3-small"

  xq = openai.Embedding.create(input=query, engine=MODEL)['data'][0]['embedding']

  res = index.query(vector = [xq], top_k=5, include_metadata=True)

  return res

def vectorQuotes(query, index):
  similarity = getRes(query, index)
  #justQuotes just uses what the query results from Pinecone itself
  justQuotes = []
  for i in range(len(similarity['matches'])):
    justQuotes.append(similarity['matches'][i]['metadata']['text'])
  return justQuotes

import openai

def getFinalSummaryGPT4(my_list, queryContext):
  my_list = my_list
  queryContext = queryContext

  # Function to split a list into equal sublists
  def split_list(lst, num_sublists):
      avg = len(lst) // num_sublists
      remainder = len(lst) % num_sublists
      return [lst[i * avg + min(i, remainder):(i + 1) * avg + min(i + 1, remainder)] for i in range(num_sublists)]

  # Split 'my_list' into n equal sublists
  n = 5
  sublists = split_list(my_list, n)

  # Generate summaries for each sublist using the OpenAI API
  sublist_summaries = []

  for i, sublist in enumerate(sublists):
      sublist_text = ' '.join(sublist)
      response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0.9,
        top_p=0.9,
        messages= [{ "role": "user", "content": queryContext+sublist_text }] )

      # Extract the summary from the API response
      summary = response.choices[0].message.content
      sublist_summaries.append(summary)

  # Combine the 10 summaries into one variable
  combined_summary = ' '.join(sublist_summaries)

  # Add a specific prompt tailored to your data
  specific_prompt = f"Given the following summaries:\n{combined_summary}\n\nGenerate a coherent final summary that captures the essence of the provided information."

  specific_prompt = queryContext + specific_prompt
  # Use OpenAI API to generate the final coherent summary

  response_combined = openai.ChatCompletion.create(
      model="gpt-4",
      temperature=0.9,
      top_p=0.9,
      messages= [{ "role": "user", "content": specific_prompt}] )

  # Extract the final summary from the API response
  final_summary = response_combined.choices[0].message.content.strip()

  return final_summary

def preprocess(query, tokens, overlap, path):
   mylist, allText = getData(tokens, overlap, path)
   index = getIndex()
   return index

def main (query, index, context):
    index = index
    contextQuery = query + context
    quotes = vectorQuotes(query, index)
    summary = getFinalSummaryGPT4(quotes, contextQuery)
    return summary

    
query = input("Enter your sustainability question: ")
context = "You are a wise AI advising about sustainability. Using the information from the text, answer the question as best as you can"
tokens = 700
overlap = 0.1
path = "combinepdf (4).pdf"
index = preprocess(query, tokens, overlap, path)
val = main(query, index, context)
print(val)


