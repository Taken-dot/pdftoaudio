import streamlit as st
import fitz
from gtts import gTTS
from pydub import AudioSegment
import os
import re

AudioSegment.converter = "/usr/bin/ffmpeg"
AudioSegment.ffprobe = "/usr/bin/ffprobe"

def clean_text(text):
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'Page \d+', '', text)
    text = re.sub(r'\d+\s*\|\s*Page', '', text)
    text = text.strip()
    return text

def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    return clean_text(text)

def chunk_text(text, chunk_size=3000):
    words = text.split()
    chunks = []
    current_chunk = ""
    
    for word in words:
        if len(current_chunk) + len(word) + 1 <= chunk_size:
            current_chunk += word + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = word + " "
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def text_to_audio(text, output_file="output.mp3"):
    chunks = chunk_text(text)
    
    if len(chunks) == 0:
        st.error("No text found in the PDF!")
        return None
    
    st.write(f"Total chunks: {len(chunks)}")
    st.write(f"Text preview: {text[:200]}")
    
    audio_segments = []
    progress = st.progress(0)
    status = st.empty()
    
    for i, chunk in enumerate(chunks):
        status.text(f"Converting chunk {i + 1} of {len(chunks)}...")
        chunk_file = f"chunk_{i}.mp3"
        tts = gTTS(text=chunk, lang="en", slow=False)
        tts.save(chunk_file)
        audio_segments.append(AudioSegment.from_mp3(chunk_file))
        os.remove(chunk_file)
        progress.progress((i + 1) / len(chunks))
    
    status.text("Stitching audio together...")
    final_audio = audio_segments[0]
    for segment in audio_segments[1:]:
        final_audio += segment
    
    final_audio.export(output_file, format="mp3")
    status.text("Done!")
    return output_file

# --- UI ---
st.set_page_config(page_title="PDF to Audio", page_icon="🎧", layout="centered")

st.title("🎧 PDF to Audio")
st.write("Convert any PDF book or document into a downloadable MP3 audiobook.")

st.divider()

uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

if uploaded_file is not None:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    doc = fitz.open("temp.pdf")
    page_count = len(doc)

    col1, col2 = st.columns(2)
    col1.metric("File name", uploaded_file.name)
    col2.metric("Pages", page_count)

    st.divider()

    if st.button("🎙️ Convert to Audio", use_container_width=True):
        text = extract_text_from_pdf("temp.pdf")
        audio_file = text_to_audio(text)

        if audio_file:
            st.success("✅ Conversion complete!")
            with open(audio_file, "rb") as f:
                st.download_button(
                    label="⬇️ Download MP3",
                    data=f,
                    file_name="audiobook.mp3",
                    mime="audio/mpeg",
                    use_container_width=True
                )