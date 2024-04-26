import io
import openai
from gtts import gTTS
import streamlit as st
from io import BytesIO
from audio_recorder_streamlit import audio_recorder

# Set page configuration
st.set_page_config(
    page_title='Speech Translation',
    page_icon='💬',
    layout='centered',
    initial_sidebar_state='auto'
)

# Hide Streamlit footer
hide_streamlit_style = """
<style>
    footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def main():
    st.header('Real Time Translation')

    # Set OpenAI API key
    openai.api_key = st.secrets["OPENAI_API_KEY"]

    audio_bytes = audio_recorder(pause_threshold=40)
    if audio_bytes:
        # Check if audio is of sufficient length
        if len(audio_bytes) > 8000:
            st.success('Audio captured correctly')
        else:
            st.warning('Audio captured incorrectly, please try again.')
        st.audio(audio_bytes, format="audio/wav")
        st.session_state.audio_bytes = audio_bytes

        if  'audio_bytes' in st.session_state and len(st.session_state.audio_bytes) > 0:
            # Translate audio bytes into English
            audio_file = io.BytesIO(st.session_state.audio_bytes)
            audio_file.name = "temp_audio_file.wav"
            transcript = openai.Audio.translate("whisper-1", audio_file)

            if transcript['text']:
                sound_file = BytesIO()
                tts = gTTS(transcript['text'], lang='en')
                tts.write_to_fp(sound_file)
                st.markdown("Synthesized Speech Translation")
                st.audio(sound_file)
                st.markdown("Translation Transcript")
                st.text_area('transcription', transcript['text'], label_visibility='collapsed')
        else:
            st.warning('No audio recorded, please ensure your audio was recorded correctly.')


if __name__ == '__main__':
    main()