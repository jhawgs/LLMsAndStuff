from llama_index.readers.youtube_transcript import YoutubeTranscriptReader
from llama_index.readers.assemblyai import AssemblyAIAudioTranscriptReader
import pandas as pd
from llama_index.core.llama_pack import download_llama_pack
from ollama_interface import gen
import streamlit as st
from docx import Document
from io import BytesIO
from fpdf import FPDF
from custom_css import add_custom_css
from custom_html import add_custom_html

API_KEY = ""

# Set page configuration
st.set_page_config(
    page_icon="📔",
    page_title="Chalkboard.ai",
    layout="centered"
)

def transcribe_local_audio(path):
    reader = AssemblyAIAudioTranscriptReader(file_path=path, api_key=API_KEY)
    return reader.load_data()

# Function to save text as .docx
def save_as_docx(text):
    doc = Document()
    doc.add_paragraph(text)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# Function to save text as .pdf
def save_as_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer

def main():
    # Add custom CSS
    add_custom_css()

    st.title("Chalkboard.ai")
    st.subheader("Note Taker for YouTube Lectures, Edit Your Notes, and Download")

    # Input for YouTube links
    links = st.text_area("Enter YouTube links (one per line):")
    links = links.splitlines()

    # Slider for detail level
    detail_level = st.slider("Detail Level", 1, 10, 5)
    
    if st.button("Generate Notes"):
        if links:
            with st.spinner("Loading transcripts..."):
                loader = YoutubeTranscriptReader()
                documents = loader.load_data(ytlinks=links)

            def doc_to_text(doc):
                return doc.text

            # Create DataFrame
            df = pd.DataFrame({"link": links, "doc": list(map(doc_to_text, documents))})
            df.to_csv("./docs.csv")

            # Generate notes using ollama_interface
            with open("./docs.csv", "r") as doc:
                detail_instruction = f"The detail level should be {detail_level}."
                if detail_level <= 3:
                    detail_instruction = "Keep the notes concise and to the point, very short. A five year old should understand this with the vocab used. Use full sentences."
                elif detail_level <= 7:
                    detail_instruction = "Include moderate details and explanations. A high school graduate should understand this with the vocab used. Use full sentences."
                else:
                    detail_instruction = "Provide extensive details, explanations, quotes, and examples. A college graduate should understand this with the vocab used. Use full sentences."

                input_text = (
                    "Format this .csv file into a chronological page of notes formatted as key points with details underneath "
                    f"{detail_instruction} {doc.read()}"
                )
                notes = gen(input_text)

            # Display the notes
            st.markdown("### Generated Notes")
            st.text_area("Notes", value=notes, height=1200)

            # Save the notes as a .docx file
            docx_buffer = save_as_docx(notes)
            st.download_button(
                label="Download Notes as .docx",
                data=docx_buffer,
                file_name="Generated_Notes.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

            # Save the notes as a .pdf file
            pdf_buffer = save_as_pdf(notes)
            st.download_button(
                label="Download Notes as .pdf",
                data=pdf_buffer,
                file_name="Generated_Notes.pdf",
                mime="application/pdf"
            )
    add_custom_html()
if __name__ == "__main__":
    main()