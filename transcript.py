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
from mongodb_handler import save_notes, get_notes_by_subject, get_subjects, delete_note  # Updated import
from audio_extract import extract_audio

API_KEY = "68b5e00bfac44433b2abc29dcf1aacaf"

# Set page configuration
st.set_page_config(
    page_icon="📔",
    page_title="Chalkboard.ai",
    layout="centered"
)

def transcribeVideo(uploaded_file):
    file_path = f"./{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    convertV2A(file_path)
    text = transcribe_local_audio("./outputAudio.mp3")
    os.remove(file_path)
    os.remove("./outputAudio.mp3")
    return text

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

# Function to save text as .pdf using a Unicode font
def save_as_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=12)
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

    # Create columns for layout
    col1, col2 = st.columns(2)

    with col1:
        # File uploader for video file
        uploaded_file = st.file_uploader("Upload a Video File", type=["mp4", "mkv", "avi", "mov"])

    with col2:
        # Input for YouTube links
        youtube_links = st.text_area("Enter YouTube links (one per line):")
        youtube_links = youtube_links.splitlines()

    col3, col4 = st.columns(2)

    with col3:
        # Slider for detail level
        detail_level = st.slider("Detail Level", 1, 10, 5)

    with col4:
        # Input for subject
        subject = st.text_input("Enter subject for the notes:")

    # Input for note name
    note_name = st.text_input("Enter a name for the notes:")

    if st.button("Generate Notes"):
        documents = []
        sources = youtube_links[:]
        
        if uploaded_file:
            documents.append(transcribeVideo(uploaded_file))
            sources.append(uploaded_file.name)

        if youtube_links:
            loader = YoutubeTranscriptReader()
            youtube_documents = loader.load_data(ytlinks=youtube_links)
            documents.extend(youtube_documents)

        if documents:
            def doc_to_text(doc):
                if isinstance(doc, list) and len(doc) > 0 and hasattr(doc[0], 'text'):
                    return doc[0].text
                return str(doc)  # Fallback to string representation if structure is unexpected

            # Create DataFrame
            df = pd.DataFrame({"source": sources, "doc": list(map(doc_to_text, documents))})
            st.write("DataFrame created:", df)
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
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                key="download_docx"
            )

            # Save the notes as a .pdf file
            pdf_buffer = save_as_pdf(notes)
            st.download_button(
                label="Download Notes as .pdf",
                data=pdf_buffer,
                file_name="Generated_Notes.pdf",
                mime="application/pdf",
                key="download_pdf"
            )

    # View notes by subject
    st.subheader("View Notes by Subject")
    subjects = get_subjects()

    # Initialize session state for expanders
    if "expanders" not in st.session_state:
        st.session_state.expanders = {}

    # Function to toggle expander state
    def toggle_expander(subject):
        if subject in st.session_state.expanders:
            st.session_state.expanders[subject] = not st.session_state.expanders[subject]
        else:
            st.session_state.expanders[subject] = True

    if st.button("All Notes"):
        notes_list = get_notes_by_subject()
        if notes_list:
            for note in notes_list:
                note_name = note.get("note_name", "Unnamed Note")
                note_id = str(note["_id"])  # Convert ObjectId to string for keys
                with st.expander(f"{note_name} ({note['subject']}) - Click to Expand/Collapse", expanded=st.session_state.expanders.get(note_name, False)):
                    st.text_area("Notes", value=note["notes"], height=400, key=f"note_{note_id}")
                    col_download, col_delete = st.columns(2)
                    with col_download:
                        docx_buffer = save_as_docx(note["notes"])
                        st.download_button(
                            label="Download Notes as .docx",
                            data=docx_buffer,
                            file_name=f"{note_name}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            key=f"download_docx_{note_id}"
                        )

                        pdf_buffer = save_as_pdf(note["notes"])
                        st.download_button(
                            label="Download Notes as .pdf",
                            data=pdf_buffer,
                            file_name=f"{note_name}.pdf",
                            mime="application/pdf",
                            key=f"download_pdf_{note_id}"
                        )
                    with col_delete:
                        if st.button("Delete", key=f"delete_{note_id}"):
                            delete_note(note_id)
                            st.experimental_rerun()

    for subj in subjects:
        if st.button(subj):
            toggle_expander(subj)
            notes_list = get_notes_by_subject(subj)
            if notes_list:
                for note in notes_list:
                    note_name = note.get("note_name", "Unnamed Note")
                    note_id = str(note["_id"])  # Convert ObjectId to string for keys
                    with st.expander(f"{note_name} - Click to Expand/Collapse", expanded=st.session_state.expanders.get(subj, False)):
                        st.text_area("Notes", value=note["notes"], height=400, key=f"note_{note_id}")
                        col_download, col_delete = st.columns(2)
                        with col_download:
                            docx_buffer = save_as_docx(note["notes"])
                            st.download_button(
                                label="Download Notes as .docx",
                                data=docx_buffer,
                                file_name=f"{note_name}.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                key=f"download_docx_{note_id}"
                            )

                            pdf_buffer = save_as_pdf(note["notes"])
                            st.download_button(
                                label="Download Notes as .pdf",
                                data=pdf_buffer,
                                file_name=f"{note_name}.pdf",
                                mime="application/pdf",
                                key=f"download_pdf_{note_id}"
                            )
                        with col_delete:
                            if st.button("Delete", key=f"delete_{note_id}"):
                                delete_note(note_id)
                                st.experimental_rerun()

    add_custom_html()

if __name__ == "__main__":
    main()
