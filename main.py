import ffmpeg
import whisper
import streamlit as st
import os

def extract_audio(input_file):
    input_file_name = os.path.splitext(input_file.name)[0]
    if input_file.type.startswith('video/'):
        extracted_audio = f"audio-{input_file_name}.wav"
        stream = ffmpeg.input("pipe:0")
        stream = ffmpeg.output(stream, extracted_audio)
        ffmpeg.run(stream, input=input_file.read(), overwrite_output=True)
        return extracted_audio
    elif input_file.type.startswith('audio/'):
        return input_file.name  
        
def main():
    st.set_page_config(
        page_title="Video to Text",
        page_icon="favicon.png",
    )   
    hide_streamlit_style = """
                <style>
                [data-testid="stToolbar"] {visibility: hidden !important;}
                header {visibility: hidden !important;}
                footer {visibility: hidden !important;}
                [data-testid="stAppViewBlockContainer"] {margin: -4.5rem; !important;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)   

    st.markdown("<h1 style='text-align: center; color: #a6e3a1;'>Video to Text</h1>", unsafe_allow_html=True)
    st.markdown("<a href='https://github.com/sameemul-haque/Video-to-Text' style='color: #6c7086; font-size: 0.9rem; text-align: center; position: fixed; top: 0; left: 0; text-decoration: none; border: solid 1px #6c7086; border-radius: 10px; padding: 0.5rem; margin: 1rem;'><img style='width: 0.9rem; filter: brightness(0) saturate(100%) invert(47%) sepia(12%) saturate(640%) hue-rotate(193deg) brightness(91%) contrast(86%); margin-top: -0.15rem' src='https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/github/github-original.svg'/> Source Code</a>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload a video or audio file here")

    if uploaded_file is not None and (uploaded_file.type.startswith('video/') or uploaded_file.type.startswith('audio/')):
        with st.spinner('Retrieving the text from the media file. Please wait...'):
            extracted_audio = extract_audio(uploaded_file)
            model = whisper.load_model("base.en")
            result = model.transcribe(extracted_audio)
        st.markdown("***")
        st.subheader("Full text from the media file")
        st.code(result["text"], language='None')
        st.markdown("***")
        st.subheader("Segments of text from the media file")
        for segment in result["segments"]:
            st.code(segment["text"], language='None')
        st.markdown("***")
    else:
        if uploaded_file is not None:
            st.error("The file type is not supported")

if __name__ == "__main__":
    main()