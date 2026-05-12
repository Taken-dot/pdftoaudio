import streamlit as st
import fitz
from gtts import gTTS
import os

def extract_text_from_pdf(pdf_path, max_pages=3):
    text = ""
    doc = fitz.open(pdf_path)
    for i, page in enumerate(doc):
        if i >= max_pages:
            break
        text += page.get_text()
    return text

def text_to_audio(text, output_file="output.mp3"):
    tts = gTTS(text=text, lang="en", slow=False)
    tts.save(output_file)
    return output_file


# --- UI ---
st.title("PDF to Audio")
st.write("Upload a PDF and convert it to an MP3 audiobook.")

uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

if uploaded_file is not None:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    st.success("File uploaded!")

    if st.button("Convert to Audio"):
        with st.spinner("Converting..."):
            text = extract_text_from_pdf("temp.pdf")
            audio_file = text_to_audio(text)

        st.success("Done!")

        with open(audio_file, "rb") as f:
            st.download_button(
                label="Download MP3",
                data=f,
                file_name="audiobook.mp3",
                mime="audio/mpeg"
            )