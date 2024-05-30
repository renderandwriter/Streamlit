import streamlit as st
import streamlit.components.v1 as components
from streamlit_webrtc import webrtc_streamer
import speech_recognition as sr

#Username & password
users = {"user1": "password1", "user2": "password2"} 

def main():
    try:
        st.set_page_config(page_title="Streamlit App", page_icon=":tada:", layout="wide")
    except Exception as e:
        st.error(f"An error occurred while setting the page configuration: {e}")
        return

    try:
        #Banner on top
        st.markdown("<h1 style='text-align: center; color: green; font-family: Roboto;'>Welcome to streamlit site</h1>", unsafe_allow_html=True)

        #Session & login check
        if 'logged_in' not in st.session_state:
            st.session_state['logged_in'] = False
        
        if not st.session_state['logged_in']:
            login()
        else:
            app_content()
    except Exception as e:
        st.error(f"An error occurred in the main function: {e}")

def login():
    try:
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username in users and users[username] == password:
                st.session_state['logged_in'] = True
                st.experimental_rerun()
            else:
                st.error("Invalid Username/Password")
    except Exception as e:
        st.error(f"An error occurred during login: {e}")

def app_content():
    try:
        #Header section
        st.subheader("My self Rajkumar Singh :wave:")
        st.subheader("A UX/UI designer who is trying to use streamlit for building website")
        st.write("[Learn more about my past work:>](https://rajkumarsingh.framer.ai/)")

        st.sidebar.title("Menu")
        if st.sidebar.button("Logout"):
            st.session_state['logged_in'] = False
            st.experimental_rerun()

        st.subheader("Enter your text below:")
        text = st.text_area("Text Input")

        #Option to copy text from a subsection of the page with just a click of a clipboard icon.
        if text:
            try:
                st.write("Click the button below to copy the text to clipboard.")
                # Text area for user input.
                components.html(f"""
                <textarea id="text" style="opacity:0;">{text}</textarea>
                <button onclick="copyToClipboard()">Copy to Clipboard</button>
                <script>
                function copyToClipboard() {{
                    var copyText = document.getElementById("text");
                    copyText.select();
                    document.execCommand("copy");
                    alert("Copied to clipboard");
                }}
                </script>
                """, height=200)
            except Exception as e:
                st.error(f"An error occurred while setting up the clipboard copy functionality: {e}")


        # Ability to enter user input through a voice command.
        st.subheader("Voice Input")
        if st.button("Start Voice Input"):
            try:
                recognizer = sr.Recognizer()
                recognizer.energy_threshold = 3000  # Adjust based on your environment
                with sr.Microphone() as source:
                    st.write("Adjusting for ambient noise, please wait...")
                    recognizer.adjust_for_ambient_noise(source, duration=4)
                    st.write("Say something...")
                    audio = recognizer.listen(source)
                    st.write("Processing...")
                text_from_voice = recognizer.recognize_google(audio)
                st.write(f"Voice Input: {text_from_voice}")
            except sr.UnknownValueError:
                st.error("Could not understand the audio. Please try again.")
            except sr.RequestError as e:
                st.error(f"Could not request results from Google Speech Recognition service; {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred; {e}")
    except Exception as e:
        st.error(f"An error occurred in the app content: {e}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"An unexpected error occurred in the main block: {e}")
