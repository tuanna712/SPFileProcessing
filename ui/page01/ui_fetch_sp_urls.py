import streamlit as st
from functions.func_sharepoint import fetch_SP_urls

def ui_fetch_SP_urls():
    fetch_SP_urls_btn = st.button("Fetch all files' urls", key='fetch_SP_urls')
    if fetch_SP_urls_btn:
        with st.spinner("Fetching all files' urls..."):
            fetch_SP_urls()