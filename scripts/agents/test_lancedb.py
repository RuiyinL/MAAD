import lancedb
import pandas as pd
import pyarrow as pa
import os
import getpass

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = "[OpenAI API Key]"

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import LanceDB
from langchain_openai import OpenAIEmbeddings
import lancedb

sec_filing_pdf = "C:\\Research\\MAAD\\demo\\demo_v4\\agents\\rag\\software-architecture-in-practice-3rd-edition.pdf"
loader = PyPDFLoader(sec_filing_pdf)
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=0)
docs = text_splitter.split_documents(documents)


embedding_function = OpenAIEmbeddings()

db = lancedb.connect("~/langchain")
table = db.open_table("vectorstore")
db = LanceDB.from_documents(docs, embedding_function, connection=db)
print("Finished loading documents into LanceDB")