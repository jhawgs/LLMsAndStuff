import streamlit as st

def add_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&display=swap');

    body {
        background-color: #1b1b1b;  /* Dark background for the chalkboard effect */
        color: #f5f5f5;  /* Light chalk-like color for text */
        font-family: 'Permanent Marker', cursive;  /* Chalk-like font */
        cursor: url('chalk_cursor.png'),auto;
    }
    .stTextArea, .stSlider, .stButton, .stTextInput, .stTitle, .stHeader, .stMarkdown {
        color: #f5f5f5;  /* Chalk-like color for text */
        background-color: #1b1b1b;  /* Dark background */
        border: 2px solid #8B4513;  /* Wooden border */
        border-radius: 4px;
        padding: 10px;
        box-shadow: 3px 3px 5px #000000;
        transition: transform 0.3s ease-in-out;
    }
    .stButton button, .stTextArea textarea, .stTextInput input {
        background-color: #1b1b1b;  /* Dark background for buttons and inputs */
        color: #f5f5f5;  /* Chalk-like color for text */
        border: 2px solid #8B4513;  /* Wooden border */
        padding: 8px 16px;  /* Padding for buttons */
        cursor: url('chalk_cursor.png'),auto;
        transition: background-color 0.3s ease;
    }
    .stButton button:hover, .stTextArea textarea:hover, .stTextInput input:hover {
        background-color: #2c2c2c;  /* Darker background on hover */
    }
    .stTitle {
        color: #f5f5f5;  /* Chalk-like color for titles */
        font-size: 2em;  /* Larger font size for titles */
        margin-bottom: 20px;  /* Bottom margin for separation */
        text-align: center;  /* Center align title */
    }
    .stHeader {
        color: #f5f5f5;  /* Chalk-like color for headers */
        opacity: 0.7;  /* Semi-faded header */
    }
    .stMarkdown h1,
    .stMarkdown h2 {
        color: #f5f5f5;  /* Chalk-like color for markdown headers */
    }
    .calendar-container {
        padding-top: 100px;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
    }
    .calendar {
        display: flex;
        flex-wrap: wrap;
        border: 2px solid #8B4513;  /* Wooden border for calendar */
        border-radius: 8px;
        overflow: hidden;
        width: 100%;
        max-width: 800px;  /* Adjust width as needed */
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
    .calendar-header {
        color: #f5f5f5;  /* Chalk-like color for header */
        font-weight: bold;
        text-align: center;
        padding: 10px;
        width: 100%;
    }
    .calendar-body {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 0;
        padding: 1px;
    }
    .calendar-day {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100px;
        width: 90px;
        border-radius: 4px;
        cursor: url('chalk_cursor.png'),auto;
        color: #f5f5f5;  /* Chalk-like color for days */
        transition: background-color 0.3s ease;
    }
    .calendar-day:hover {
        background-color: #2c2c2c;  /* Darker background on hover */
    }
    .chalk-piece {
        width: 10px;
        height: 30px;
        background-color: white;
        position: absolute;
        bottom: 10px;
        left: 10px;
        transform: rotate(-45deg);
        box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)
