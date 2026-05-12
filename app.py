import streamlit as st
import fitz
from gtts import gTTS
from pydub import AudioSegment
import os

AudioSegment.converter = "/usr/bin/ffmpeg"
AudioSegment.ffprobe = "/usr/bin/ffprobe"


def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    return text

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
    audio_segments = []
    
    for i, chunk in enumerate(chunks):
        chunk_file = f"chunk_{i}.mp3"
        tts = gTTS(text=chunk, lang="en", slow=False)
        tts.save(chunk_file)
        audio_segments.append(AudioSegment.from_mp3(chunk_file))
        os.remove(chunk_file)
    
    final_audio = audio_segments[0]
    for segment in audio_segments[1:]:
        final_audio += segment
    
    final_audio.export(output_file, format="mp3")
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
        with st.spinner("Converting... this may take a few minutes for long books"):
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