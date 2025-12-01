import streamlit as st
import re

# Load secrets
API_KEY = st.secrets["API_KEY"]
PROMPT = st.secrets["PROMPT"]

# Configure Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

st.title("📘 Math Solver with LLM (LaTeX Enhanced)")

user_query = st.text_area("Enter your math problem:")

def render_with_latex(text: str):
    """Render text while detecting LaTeX expressions automatically."""
    # Match anything inside [ ... ] or $$ ... $$ or \( ... \)
    latex_patterns = re.findall(r"\[([^\]]+)\]|\$\$([^$]+)\$\$|\\\((.*?)\\\)", text)

    st.markdown("### Solution")

    # Stream full answer with proper rendering
    for line in text.split("\n"):
        line_strip = line.strip()

        # If line looks like LaTeX, render it properly
        if (
            line_strip.startswith("[") and line_strip.endswith("]") or
            line_strip.startswith("$$") and line_strip.endswith("$$") or
            re.match(r"\\\(.+\\\)", line_strip)
        ):
            content = (
                line_strip.strip("[]$")
                .replace("\\(", "")
                .replace("\\)", "")
            )
            st.latex(content)
        else:
            st.markdown(line_strip)

if st.button("Solve"):
    full_prompt = f"{PROMPT}\nUser:\n{user_query}"
    
    response = model.generate_content(full_prompt)
    output = response.text

    render_with_latex(output)
