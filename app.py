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
from ui.page01_main import display_01_main
from ui.page02_main import display_02_main

if st.session_state.get('switch_button', False):
    st.session_state['menu_option'] = (st.session_state.get('menu_option', 0) + 1) % 4
    manual_select = st.session_state['menu_option']
else:
    manual_select = None
    
# Link to Github: https://github.com/victoryhb/streamlit-option-menu
menu_selection = option_menu(None, ["Files", "Processing",],
    icons=['archive', 'card-image', "table",], #, 'blockquote-right'
    orientation="horizontal", manual_select=manual_select, key='menu_4',
    styles={
        # "container": {"padding": "0!important", "background-color": "#fafafa"},
        # "nav-link-selected": {"background-color": "green"},
    }
    )

if menu_selection == "Files":
    display_01_main()
elif menu_selection == "Processing":
    display_02_main()

