from PIL import Image
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
logo = Image.open("./assets/images/logo.png")
st.set_page_config(# Alternate names: setup_page, page, layout
                layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
                initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
                page_title="SP File Processing",  # String or None. Strings get appended with "• Streamlit". 
                page_icon=logo,  # String, anything supported by st.image, or None.
                )

# --- LOAD CSS ------------------------------------------------------------------
with open("./style/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- MAIN ----------------------------------------------------------------------
from streamlit_option_menu import option_menu
