import json, os
from .core.connectors import Connector
from .params import *

import warnings
warnings.filterwarnings("ignore", category=ResourceWarning)

def fetch_SP_urls():
    # Connect to Sharepoint
    SPConnector = Connector().to_sharepoint()

    # Get all files' links
    file_links, _ = SPConnector._get_all_files_links()
    
    #Send notification
    print(f"Found {len(file_links)} files.\n")

    # Define a list to store all urls
    _all_urls = []

    # Check TARGET_FOLDER
    if len(TARGET_FOLDER) == 0: # If TARGET_FOLDER is empty, get all files from MAIN_SITE
        _urls = [url for url in file_links if url.startswith(MAIN_SITE)]
        _all_urls.extend(_urls)

        # Send notification
        print(f"Found {len(_all_urls)} files from {MAIN_SITE}.\n")

    else: # Otherwise, get files in TARGET_FOLDER
        for folder in TARGET_FOLDER:
            TARGET_FOLDER_URL = MAIN_SITE + folder
            _urls = [url for url in file_links if url.startswith(TARGET_FOLDER_URL)]
            _all_urls.extend(_urls)

            # Send notification
            print(f"Found {len(_all_urls)} files from {folder}.\n")

    # Convert data to dictionary
    _urls_dict = {i: _all_urls[i] for i in range(len(_all_urls))}

    # Save URLs to JSON file
    __save_json(FETCHED_MAINSITE_FILE_URLS_JSON, _urls_dict)

def __save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f)
    print(f"Saved data to {path}")

def __load_json(path):
    with open(path, "r") as f:
        return json.load(f)
    print(f"Loaded data from {path}")