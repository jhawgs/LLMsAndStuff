from pymongo import MongoClient
import streamlit as st

# MongoDB connection setup
def get_db_connection():
    client = MongoClient(
        "mongodb+srv://dstutz:QulJC71ClrdoSIYi@chalkboarddb.ablhj7x.mongodb.net/?retryWrites=true&w=majority&appName=chalkboardDB",
        tls=True,
        tlsAllowInvalidCertificates=True
    )
    db = client["chalkboard_db"]
    return db

def save_notes(subject, note_name, notes):
    db = get_db_connection()
    notes_collection = db["notes"]
    notes_data = {
        "subject": subject,
        "note_name": note_name,
        "notes": notes
    }
    notes_collection.insert_one(notes_data)
    st.success("Notes saved successfully!")

def get_notes_by_subject(subject=None):
    db = get_db_connection()
    notes_collection = db["notes"]
    if subject:
        notes = notes_collection.find({"subject": subject})
    else:
        notes = notes_collection.find()
    return list(notes)

def get_subjects():
    db = get_db_connection()
    notes_collection = db["notes"]
    subjects = notes_collection.distinct("subject")
    return subjects
