import json, os
import streamlit as st
from .core.connectors import Connector
from .params import FETCHED_SITE_FILE_URLS_JSON

import warnings
warnings.filterwarnings("ignore", category=ResourceWarning)

def fetch_all_files_urls():
    SPConnector = Connector().to_sharepoint()
    file_links, _ = SPConnector._get_all_files_links()

    #Send notification
    print(f"Found {len(file_links)} files.\n")

    # Convert data to dictionary
    _urls_dict = {i: file_links[i] for i in range(len(file_links))}

    # Save URLs to JSON file
    save_json(FETCHED_SITE_FILE_URLS_JSON, _urls_dict)

def get_file_urls_by_folder(targeted_folder, parent_url, urls_path):
    # Check if FETCHED_SITE_FILE_URLS_JSON exists
    if not os.path.exists(FETCHED_SITE_FILE_URLS_JSON):
        print(f"{FETCHED_SITE_FILE_URLS_JSON} not found. Fetching all files' urls...")
        fetch_all_files_urls()
    
    # Load data from JSON file
    fetched_site_files = load_json(FETCHED_SITE_FILE_URLS_JSON)
    print(f"Loaded data from {FETCHED_SITE_FILE_URLS_JSON}: {len(fetched_site_files)} files.")

    # Convert data to list
    file_links = list(fetched_site_files.values())

    # Filter file urls by targeted_folder
    # Define a list to store all urls
    _all_urls = []

    # Check TARGET_FOLDER
    if len(targeted_folder) == 0: # If TARGET_FOLDER is empty, get all files from MAIN_SITE
        _urls = [url for url in file_links if url.startswith(parent_url)]
        _all_urls.extend(_urls)

        # Send notification
        print(f"Found total {len(_all_urls)} files. Just added {len(_urls)} files from {parent_url}.\n")

    else: # Otherwise, get files in TARGET_FOLDER
        for folder in targeted_folder:
            targeted_folder_url = parent_url + folder
            _urls = [url for url in file_links if url.startswith(targeted_folder_url)]
            _all_urls.extend(_urls)

            # Send notification
            print(f"Found total {len(_all_urls)} files. Just added {len(_urls)} files from {folder}.\n")

    # Convert data to dictionary
    _urls_dict = {i: _all_urls[i] for i in range(len(_all_urls))}

    # Save URLs to JSON file
    save_json(urls_path, _urls_dict)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f)
    print(f"Saved data to {path}")

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)
    print(f"Loaded data from {path}")

def get_metadata_pdf_files(urls_path, output_path):
    SPConnector = Connector().to_sharepoint()
    # Load json file
    with open(urls_path, "r") as f:
        urls_dict = json.load(f)

    all_file_meta = []
    for i, url in enumerate(list(urls_dict.values())):
        if i%10==0:
            print(f"Processing {i+1}/{len(urls_dict)}")
            st.success(f"Processing {i+1}/{len(urls_dict)}")
        if url.endswith('.pdf'):
            try:
                file_meta = SPConnector.get_metadata(url)
                all_file_meta.append(file_meta)
            except Exception as e:
                print(e)
                continue
        
    chatbot_files =[meta for meta in all_file_meta if meta['Function'] == 'Chatbot' and meta ['TypeOfFile'] =='Digital']

    chatbot_urls = {}
    for i, file in enumerate(chatbot_files):
        chatbot_urls[str(i)]=file['ServerRelativeUrl']

    #Save to json file
    with open(output_path, "w") as f:
        json.dump(chatbot_urls, f)

    print(len(chatbot_files))