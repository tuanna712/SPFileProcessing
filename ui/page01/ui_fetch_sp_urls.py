import json
import streamlit as st
from functions.func_sharepoint import fetch_all_files_urls, get_file_urls_by_folder, get_metadata_pdf_files
from functions.params import FETCHED_SITE_FILE_URLS_JSON

SONGHONG_URL_PATH = "data/songhong_file_urls.json"
ALL_SITE_URL_PATH = FETCHED_SITE_FILE_URLS_JSON
SONGHONG_PDF_4BOT = "data/songhong_files_4bot.json"
PROCESSED_IMG_FILE_ID = "data/processed_img_file_id.json"
PROCESSED_IMG_FILE_URLS = "data/processed_img_file_urls.json"

def ui_fetch_site_urls():
    fetch_site_urls_btn = st.button("Fetch ALL SITE", key='fetch_site_urls')
    if fetch_site_urls_btn:
        with st.spinner("Fetching ALL SITE files' urls..."):
            fetch_all_files_urls()
            st.success("Done fetching ALL SITE files' urls!")

def ui_fetch_files4bot():
    fetch_site_urls_btn = st.button("Fetch PDFs for BOT", key='fetch_files4bot')
    if fetch_site_urls_btn:
        with st.spinner("Fetching..."):
            get_metadata_pdf_files(SONGHONG_URL_PATH, SONGHONG_PDF_4BOT)
            st.success("Done PDF files' urls!")

def ui_fetch_processed_image():
    fetch_processed_img_files_btn = st.button("Fetch Processed IMG files", key='fetch_processed_img_files_btn')
    if fetch_processed_img_files_btn:
        with st.spinner("Fetching..."):
            targeted_folder = ["PROCESSED_IMAGES"]
            parent_url = "/sites/Eptesting/Shared Documents/General/PROCESSED_DATA/"
            urls_path = PROCESSED_IMG_FILE_URLS
            get_file_urls_by_folder(targeted_folder, parent_url, urls_path)
            st.success("Done fetching SONGHONG files' urls!")
        with open(PROCESSED_IMG_FILE_URLS, "r") as f:
            processed_img_files = json.load(f)
        file_id_list = []
        for i, url in processed_img_files.items():
            file_id = url.split('/')[7]
            file_id_list.append(file_id)
        file_id_unique = list(set(file_id_list))
        for id in file_id_unique:
            st.info(f"Image Processed File ID: {id}")
        file_id_dict = {i: file_id_unique[i] for i in range(len(file_id_unique))}
        with open(PROCESSED_IMG_FILE_ID, "w") as f:
            json.dump(file_id_dict, f)


def ui_fetch_songhong_urls():
    fetch_songhong_urls_btn = st.button("Fetch SONG HONG BASIN", key='fetch_songhong_urls')
    if fetch_songhong_urls_btn:
        with st.spinner("Fetching SONGHONG files' urls..."):
            targeted_folder = ["1. Regional Studies",
                "Block 100-101",
                "Block 102-106",
                "Block 103-107",
                "Block 104",
                "Block 105",
                "Block 108",
                "Block 111",
                "Block 112",
                "Block 113",
                "Block 114",
                "Block 115",
                "Block 117",
                "Block 118",
                "Block 119",
                "Block 120",
                "Block 121",
                "MVHN 01 02KT",
                "MVHN 02",
                ]
            parent_url = "/sites/Eptesting/Shared Documents/General/DATABASE/Song Hong Basin/"
            urls_path = SONGHONG_URL_PATH
            get_file_urls_by_folder(targeted_folder, parent_url, urls_path)
            st.success("Done fetching SONGHONG files' urls!")

