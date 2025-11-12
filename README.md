# 📘 AI PDF-to-HTML Converter

This is a Streamlit web application that converts technical PDF datasheets into structured, semi-styled HTML.

It works by extracting all text, tables, and images from an uploaded PDF. It then sends this extracted content to a Google Generative AI model (Gemini) with a prompt to rebuild the content as a semantic HTML page, complete with inline CSS to visually resemble the original document.

## Features

* **PDF Upload:** A simple interface to upload any PDF file.
* **Content Extraction:** Uses `pdfplumber` for text/tables and `PyMuPDF` for images.
* **AI Conversion:** Leverages a Generative AI model (`gemini-1.5-flash`) to intelligently structure the content into semantic HTML (`<h1>`, `<table>`, `<p>`, etc.).
* **Image Handling:** Embeds extracted images directly into the HTML using Base64 encoding.
* **HTML Preview:** Displays the final generated HTML directly in the app.
* **Download:** Allows you to download the final `*.html` file.

## 🚀 How to Run

### 1. Prerequisites

You'll need Python 3.8 or newer.

### 2. Setup Project

1.  **Create a project folder** and save your `app.py` file inside it.

2.  **Create a virtual environment** (recommended):
    ```bash
    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # On Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install dependencies:**
    Create a file named `requirements.txt` in your project folder and add the following lines:
    ```
    streamlit
    pdfplumber
    PyMuPDF
    langchain-google-genai
    pillow
    ```
    Then, install them all by running:
    ```bash
    pip install -r requirements.txt
    ```

### 3. Set Your API Key

This project uses the Google Generative AI API.

1.  Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
2.  Set it as an environment variable named `GOOGLE_API_KEY`.

    * **On macOS/Linux:**
        ```bash
        export GOOGLE_API_KEY='Your_API_Key_Here'
        ```
    * **On Windows (Command Prompt):**
        ```bash
        set GOOGLE_API_KEY=Your_API_Key_Here
        ```
    * **On Windows (PowerShell):**
        ```bash
        $env:GOOGLE_API_KEY="Your_API_Key_Here"
        ```

    **Note:** You must set this variable in the *same terminal session* where you will run the Streamlit app.
