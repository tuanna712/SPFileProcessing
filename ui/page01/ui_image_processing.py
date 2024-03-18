import json, os
import streamlit as st
from functions.func_sharepoint import load_json, save_json
from functions.core.connectors import Connector
SONGHONG_PDF_4BOT = "data/songhong_files_4bot.json"
PROCESSED_IMG_FILE_ID = "data/processed_img_file_id.json"

def doSomeThing():
    SPConnector = Connector().to_sharepoint()

    processed_urls = list(load_json(PROCESSED_IMG_FILE_ID).values())
    processing_url = load_json(SONGHONG_PDF_4BOT)

    for url in processing_url:
        file_info = SPConnector.get_metadata(url)
        info_dict = __info_dict(file_info)

def __info_dict(file_info):
    return {
            'file_id': file_info['GUID'],
            'file_name': file_info['Name'],
            'file_extension': file_info['Name'].split('.')[-1],
            'file_link_url': file_info['LinkingUri'],
            'file_redirect_url': file_info['ServerRedirectedEmbedUri'],
            'file_sever_relative_url': file_info['ServerRelativeUrl'],
            'status': 'unprocessed',
        }