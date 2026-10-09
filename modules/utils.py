from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

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

def disable_selectbox_typing() -> None:
    """
    Disables keyboard typing and mobile on-screen keyboards in Streamlit selectboxes.
    Sets `readOnly` and `inputmode='none'` on all selectbox input elements so that
    widgets behave strictly as click-to-select dropdown menus.
    """
    js_code = """
    <script>
    const disableTyping = () => {
        try {
            const parentDoc = window.parent.document;
            if (!parentDoc) return;
            const inputs = parentDoc.querySelectorAll('[data-testid="stSidebar"] [data-testid="stSelectbox"] input, [data-testid="stSelectbox"] input');
            inputs.forEach(input => {
                if (!input.readOnly) {
                    input.readOnly = true;
                    input.setAttribute('inputmode', 'none');
                    input.style.caretColor = 'transparent';
                    input.style.cursor = 'pointer';
                    input.addEventListener('keydown', (e) => {
                        if (!['Tab', 'Escape', 'ArrowUp', 'ArrowDown', 'Enter'].includes(e.key)) {
                            e.preventDefault();
                            e.stopPropagation();
                        }
                    }, true);
                }
            });
        } catch (err) {
            // Gracefully ignore if cross-origin iframe security applies
        }
    };

    disableTyping();
    try {
        const observer = new MutationObserver(disableTyping);
        observer.observe(window.parent.document.body, { childList: true, subtree: true });
    } catch (e) {}
    </script>
    """
    components.html(js_code, height=0, width=0)
