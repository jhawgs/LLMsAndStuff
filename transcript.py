import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from llama_index.readers.youtube_transcript import YoutubeTranscriptReader
from llama_index.readers.assemblyai import AssemblyAIAudioTranscriptReader
import assemblyai as aai
import pandas as pd
from llama_index.core.llama_pack import download_llama_pack
from ollama_interface import gen
import streamlit as st
from docx import Document
from io import BytesIO
from fpdf import FPDF
from custom_css import add_custom_css
from custom_html import add_custom_html
from mongodb_handler import save_notes, get_notes_by_subject, get_subjects  # Updated import
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
from audio_extract import extract_audio
import os

API_KEY = "68b5e00bfac44433b2abc29dcf1aacaf"

# Set page configuration
st.set_page_config(
    page_icon="📔",
    page_title="Chalkboard.ai",
    layout="centered"
)


def transcribeVideo(path):
    convertV2A(path)
    text = transcribe_local_audio("./outputAudio.mp3")
    os.system("rm ./outputAudio.mp3")
    print(text)

def convertV2A(inputVideoFile):
    extract_audio(input_path=inputVideoFile, output_path="./outputAudio.mp3")

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

    # Input for subject
    subject = st.text_input("Enter subject for the notes:")

    # Input for note name
    note_name = st.text_input("Enter a name for the notes:")

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

            if subject and note_name:
                # Save the notes to MongoDB
                save_notes(subject, note_name, notes)

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

    # View notes by subject
    st.subheader("View Notes by Subject")
    subjects = get_subjects()

    if st.button("All Notes"):
        notes_list = get_notes_by_subject()
        if notes_list:
            for note in notes_list:
                note_name = note.get("note_name", "Unnamed Note")
                with st.expander(f"{note_name} ({note['subject']}) - Click to Expand/Collapse"):
                    st.text_area("Notes", value=note["notes"], height=400)
                    if st.button("Close", key=f"close_{note['_id']}"):
                        st.text_area("Notes", value="", height=0)

    for subj in subjects:
        if st.button(subj):
            notes_list = get_notes_by_subject(subj)
            if notes_list:
                for note in notes_list:
                    note_name = note.get("note_name", "Unnamed Note")
                    with st.expander(f"{note_name} - Click to Expand/Collapse"):
                        st.text_area("Notes", value=note["notes"], height=400)
                        if st.button("Close", key=f"close_{note['_id']}"):
                            st.text_area("Notes", value="", height=0)
            else:
                st.warning(f"No notes found for subject: {subj}")

    add_custom_html()

if __name__ == "__main__":
    main()
