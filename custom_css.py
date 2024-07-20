import streamlit as st
def add_custom_css():
    st.markdown("""
    <style>
    body {
        background-color: #000000;  /* Black background for the entire page */
        color: #FFFFFF;  /* White text color */
        font-family: Arial, sans-serif;  /* Default font */
    }
    .stTextArea, .stSlider, .stButton {
        color: #FFFFFF;  /* White text color */
        border: none;  /* No border */
    }
    .stTextArea textarea, .stTextInput input {
        /* No specific styles defined here */
    }
    .stButton button {
        background-color: #333333;  /* Dark gray background for buttons */
        color: #FFFFFF;  /* White text color for buttons */
        padding: 8px 16px;  /* Padding for buttons */
        cursor: pointer;  /* Pointer cursor on hover */
    }
    .stButton button:hover {
        background-color: #555555;  /* Lighter gray background when hovering over buttons */
    }
    .stTitle {
        color: #CCCCCC;  /* Light gray color for titles */
        font-size: 2em;  /* Larger font size for titles */
        margin-bottom: 20px;  /* Bottom margin for separation */
        text-align: center;  /* Center align title */
    }
    .stHeader {
        color: #CCCCCC;  /* Light gray color for headers */
        opacity: 0.7;  /* Semi-faded header */
    }
    .stMarkdown h1,
    .stMarkdown h2 {
        color: #CCCCCC;  /* Light gray color for markdown headers */
    }
    .calendar-container {
        padding-top: 100px;
        display: flex;
        justify-content: right;
        align-items: center;
        margin-bottom: 20px;
    }
    .calendar {
        justify-content: center;
        display: flex;
        flex-wrap: wrap;
        border: 0px solid #CCCCCC;
        border-radius: 8px;
        overflow: hidden;
        width: 100%;
        max-width: 800px;  /* Adjust width as needed */
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }
    .calendar-header {
        
        color: #FFFFFF;
        font-weight: bold;
        text-align: center;
        padding: 10px;
        width: 100%;
    }
    .calendar-body {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 0px;
        padding: 1 px;
    }
    .calendar-day {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100px;
        width: 90px;
        border-radius: 4px;
        cursor: pointer;
        color: #FFFF;  /* Black text color */
    }
    .calendar-day:hover {
        background-color: #CCCCCC;
    }
    </style>
    """, unsafe_allow_html=True)