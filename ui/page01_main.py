import os, json
import streamlit as st
from functions.params import *
# from functions.core.connectors import Connector
# from functions.core.mongodb import MGCollection
# from functions.core.weaviatedb import WVCollection
# from functions.core.open_ai import MyOAI

from dotenv import load_dotenv
load_dotenv()

#-----------------------------------------------------------------------------
# #Connect to OpenAI
# OAI = MyOAI(os.environ.get('OPENAI_API_KEY'))
# #Connect to Weaviate
# WVClient = WVCollection(mode='cloud', collection_name=WEAVIATE_COLL_NAME, URL=WEAVIATE_URL, API_KEY=WEAVIATE_API_KEY)
# #Connect to MongoDB
# MGC_PROCESS = MGCollection(db_name=MONGODB_NAME, collection_name=MG_PROCESS_COLL)
# MGC_IMAGE = MGCollection(db_name=MONGODB_NAME, collection_name=MG_IMAGE_COLL)
# MGC_TABLE = MGCollection(db_name=MONGODB_NAME, collection_name=MG_TABLE_COLL)
# #Connect to Sharepoint
# SPConnector = Connector().to_sharepoint()
#-----------------------------------------------------------------------------
from .page01.ui_fetch_sp_urls import ui_fetch_SP_urls
def display_01_main():
    ui_fetch_SP_urls()
    ...
