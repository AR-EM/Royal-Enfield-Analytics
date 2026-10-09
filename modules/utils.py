from pathlib import Path
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent

def load_css(css_rel_path: str = "assets/style.css") -> None:
    """
    Reads a local CSS file and injects it into the Streamlit app.
    
    Parameters:
        css_rel_path (str): Relative file path to the CSS file from project root.
    """
    css_path = BASE_DIR / css_rel_path
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"Stylesheet not found at {css_path}")

def render_html(html_rel_path: str) -> None:
    """
    Reads a local HTML component file and injects it into the Streamlit app.
    
    Parameters:
        html_rel_path (str): Relative file path to the HTML file from project root.
    """
    html_path = BASE_DIR / html_rel_path
    if html_path.exists():
        with open(html_path, "r", encoding="utf-8") as f:
            st.markdown(f.read(), unsafe_allow_html=True)
    else:
        st.warning(f"HTML component not found at {html_path}")
