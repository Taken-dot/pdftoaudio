import fitz  # this is PyMuPDF, fitz is just its import name
from gtts import gTTS
import os

def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)

    for page in doc:
        text += page.get_text()

    return text

def text_to_audio(text, output_file="output.mp3"):
    tts = gTTS ( text=text, lang="en", slow=False)
    tts.save(output_file)
    print(f"Audio saved as {output_file}")

if __name__ == "__main__":
    text = extract_text_from_pdf("test.pdf")
    print(text[:500])  # still prints so you can see it
    text_to_audio(text)


'''What this does:
Opens your PDF file
Loops through every page
Grabs the text from each page and adds it to one big string
Returns all the text together'''

