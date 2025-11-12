import streamlit as st
import pdfplumber
import fitz  # PyMuPDF
import base64
from langchain_google_genai import ChatGoogleGenerativeAI
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="AI PDF → Structured HTML Converter", layout="wide")
st.title("📘 AI-Powered PDF → Structured HTML Converter")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    st.info("📄 Extracting text, tables, and images...")

    # ---------- TEXT & TABLE EXTRACTION ----------
    full_text = ""
    all_tables = []

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            full_text += page.extract_text() or ""
            table = page.extract_table()
            if table:
                all_tables.append(table)
    
    # ---------- IMAGE EXTRACTION ----------
    uploaded_file.seek(0)
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    images_html = ""
    image_count = 0

    for i, page in enumerate(doc):
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_img = doc.extract_image(xref)
            image_data = base_img["image"]
            image_ext = base_img["ext"]

            # Convert to base64
            image_base64 = base64.b64encode(image_data).decode("utf-8")
            images_html += f'<img src="data:image/{image_ext};base64,{image_base64}" alt="PDF Image {img_index}" style="max-width:100%; margin:10px 0;"/>'
            image_count += 1

    st.success(f"✅ Extracted {len(all_tables)} tables and {image_count} images!")

    # ---------- PREPARE LLM PROMPT ----------
    formatted_tables = ""
    for t in all_tables:
        formatted_tables += "\n".join(
            [" | ".join([str(cell) if cell else "" for cell in row]) for row in t]
        ) + "\n\n"


    prompt = f"""
    You are an expert in converting technical datasheets into structured HTML.

    Your task:
    - Convert the extracted text and tables below into a semantic, styled HTML page.
    - Use appropriate tags (<h1>, <h2>, <p>, <table>, <tr>, <td>, <img>).
    - Include provided images in logical positions.
    - Use inline CSS to make it look visually similar to the original layout.

    ========== TEXT CONTENT ==========
    {full_text}

    ========== TABLE DATA ==========
    {formatted_tables if formatted_tables else 'No tables detected.'}

    ========== IMAGE TAGS ==========
    {images_html if images_html else 'No images detected.'}

    Return only the final HTML page (no explanations).
    """

    # ---------- LLM GENERATION ----------
    with st.spinner("🧠 Generating HTML with LLM..."):
        response = ChatGoogleGenerativeAI(model="gemini-2.5-flash", messages=[
            {"role": "system", "content": "You are a professional document-to-HTML converter."},
            {"role": "user", "content": prompt}
        ])
        html_output = response["message"]["content"]

    # ---------- SHOW RESULTS ----------
    st.subheader("🧾 Generated HTML Preview")
    st.components.v1.html(html_output, height=600, scrolling=True)

    # ---------- DOWNLOAD ----------
    st.download_button(
        label="💾 Download HTML file",
        data=html_output,
        file_name="converted_datasheet.html",
        mime="text/html"
    )
