import streamlit as st
from gtts import gTTS
import os
import base64
import tempfile

st.set_page_config(
    page_title="Text to Speech Converter",
    page_icon="🔊",
    layout="centered"
)

def text_to_speech(text, language='en', slow=False):
    """Convert text to speech using Google Text-to-Speech"""
    try:
        tts = gTTS(text=text, lang=language, slow=slow)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tts.save(tmp_file.name)
            tmp_path = tmp_file.name
            
        return tmp_path
    
    except Exception as e:
        st.error(f"Error during text-to-speech conversion: {str(e)}")
        return None

def get_binary_file_downloader_html(bin_file, file_label='File'):
    """Generate a download link for a file"""
    with open(bin_file, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    return f'<a href="data:audio/mp3;base64,{b64}" download="{file_label}.mp3">Download {file_label}</a>'

def get_language_options():
    """Return a dictionary of supported languages"""
    return {
        'English': 'en',
        'Spanish': 'es',
        'French': 'fr',
        'German': 'de',
        'Italian': 'it',
        'Portuguese': 'pt',
        'Russian': 'ru',
        'Japanese': 'ja',
        'Korean': 'ko',
        'Chinese': 'zh-CN',
        'Hindi': 'hi',
        'Arabic': 'ar'
    }

st.title("🔊 Text to Speech Converter")

text_input = st.text_area("Enter your text here:", height=150)

languages = get_language_options()
selected_language_name = st.selectbox("Select language:", list(languages.keys()))
selected_language_code = languages[selected_language_name]

if st.button("Convert to Speech"):
    if not text_input.strip():
        st.warning("Please enter some text to convert.")
    else:
        with st.spinner("Converting text to speech..."):
            speech_file = text_to_speech(
                text=text_input,
                language=selected_language_code,
            )
            
            if speech_file:
                st.success("Conversion complete!")
                
                st.subheader("Listen")
                st.audio(speech_file, format='audio/mp3')
                
                st.subheader("Download")
                st.markdown(
                    get_binary_file_downloader_html(speech_file, 'text_to_speech'),
                    unsafe_allow_html=True
                )
                
                os.unlink(speech_file)

st.markdown("---")
