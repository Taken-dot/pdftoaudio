# 🎧 PDF to Audio

A web app that converts any PDF or text-based document into a downloadable MP3 audiobook — completely free, no account or API key required.

**Live demo:** [pdf2audio.streamlit.app](https://pdf2audio.streamlit.app)

---

## Features

- Upload any text-based PDF and convert it to an MP3 in minutes
- Handles full-length books by splitting text into chunks and stitching the audio back together
- Cleans extracted text to remove page numbers, headers, and formatting noise
- Live progress bar showing conversion status chunk by chunk
- Shows file name and page count before converting
- Downloadable MP3 output
- Free to use — powered by Microsoft Edge TTS, no API key needed

---

## Tech Stack

- **Python**
- **Streamlit** — web app UI
- **PyMuPDF (fitz)** — PDF text extraction
- **Edge TTS** — free neural text-to-speech (Microsoft)
- **pydub + ffmpeg** — audio stitching

---

## Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/Taken-dot/pdftoaudio
cd pdftoaudio
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Install ffmpeg**
```bash
sudo apt-get install ffmpeg -y
```

**4. Run the app**
```bash
streamlit run app.py
```

---

## Limitations

- Only works with text-based PDFs — scanned or image-based PDFs have no text layer and cannot be converted
- Very large books may take a few minutes to process

---

## Future Improvements

- Support for ePub format
- Voice selection (language, gender, accent)
- Speed control (slow / normal / fast)
- Chapter detection and split audio by chapter
- Audio player in the browser before downloading

---

Built by [Aparna](https://github.com/Taken-dot)
