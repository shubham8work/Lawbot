import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
from utils import create_qa_pipeline
import requests
import sqlite3
import random
import string

# Set page configuration
st.set_page_config(page_title="Indian Law Q&A Bot", page_icon="⚖")

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None
if "debug" not in st.session_state:
    st.session_state.debug = False

# Function to get database connection
def get_db_connection():
    conn = sqlite3.connect('auth.db')  # Replace with your database file path
    return conn

# Function to show signup page
def show_signup_page():
    st.title("LawBot - User Signup")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        if username and email and password:
            response = requests.post("http://127.0.0.1:5000/signup", json={
                "username": username,
                "email": email,
                "password": password
            })
            if response.status_code == 201:
                st.success("User registered successfully! Please log in.")
            else:
                st.error(response.json().get("error", "An error occurred during signup."))
        else:
            st.error("All fields are required.")

    if st.button("Go to Login"):
        st.session_state.authenticated = False


# Function to show login page
def show_login_page():
    st.title("LawBot - User Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Log In"):
        if username and password:
            response = requests.post("http://127.0.0.1:5000/login", json={
                "username": username,
                "password": password
            })

            if st.session_state.debug:
                st.write(f"Response Code: {response.status_code}")
                st.write(f"Response Text: {response.text}")

            if response.status_code == 200:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.success("Login successful!")
            else:
                st.error(response.json().get("error", "Invalid credentials. Please try again."))
        else:
            st.error("All fields are required.")

    if st.button("Go to Signup"):
        st.session_state.authenticated = False


# Function to show forgot password page
def show_forgot_password_page():
    st.title("Forgot Password")

    email = st.text_input("Enter your registered email")

    if st.button("Send Reset Link"):
        if email:
            response = requests.post("http://127.0.0.1:5000/forgot_password", json={"email": email})
            if response.status_code == 200:
                st.success("Password reset link sent to your email.")
            else:
                st.error(response.json().get("error", "Failed to send reset link"))
        else:
            st.error("Please enter your registered email.")


# Function to load the QA pipeline
def load_qa_pipeline():
    if not st.session_state.qa_chain:
        with st.spinner("Loading AI model... This might take a moment"):
            try:
                st.session_state.qa_chain = create_qa_pipeline()
            except Exception as e:
                st.error(f"Failed to load the QA pipeline: {e}")


# Function to show the chatbot
def show_chat_page():
    # Load QA pipeline
    load_qa_pipeline()

    # Page title and description
    st.title(f"🏛 Indian Law Q&A Assistant - Welcome {st.session_state.username}")
    st.write("Ask questions about Indian Law. Our AI will help you find answers from legal documents.")

    # Chat input
    user_input = st.chat_input("Ask a question about Indian Law...")
    if user_input:
        try:
            response = st.session_state.qa_chain.invoke({"query": user_input})
            bot_output = response.get('result', "I couldn't find an answer to your question.")
            
            # Add to chat log
            st.session_state.chat_log.append({"User": user_input, "Bot": bot_output})
        except Exception as e:
            st.error(f"An error occurred: {e}")

    # Display chat history
    for exchange in st.session_state.chat_log:
        with st.chat_message("user"):
            st.write(exchange["User"])
        with st.chat_message("assistant"):
            st.write(exchange["Bot"])


# Function to show logout button
def show_logout_button():
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.chat_log = []
        st.success("You have been successfully logged out.")


# Main logic
if st.session_state.authenticated:
    show_logout_button()
    show_chat_page()
else:
    st.title("LawBot - Your Legal Assistant")
    option = st.radio("Choose an option:", ["Login", "Signup", "Forgot Password"])
    if option == "Signup":
        show_signup_page()
    elif option == "Forgot Password":
        show_forgot_password_page()
    else:
        show_login_page()
