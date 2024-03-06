import ffmpeg
import whisper
import streamlit as st
import os

def extract_audio(input_video):
    input_video_name = os.path.splitext(input_video.name)[0]
    extracted_audio = f"audio-{input_video_name}.wav"
    stream = ffmpeg.input("pipe:0")
    stream = ffmpeg.output(stream, extracted_audio)
    ffmpeg.run(stream, input=input_video.read(), overwrite_output=True)
    return extracted_audio

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
                [data-testid="stAppViewBlockContainer"] {margin: -5rem; !important;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)   
    # st.link_button("Source Code - GitHub", "https://github.com/sameemul-haque/Video-to-Text")

    # st.title('Video to Text')
    st.markdown("<h1 style='text-align: center; color: #a6e3a1;'>Video to Text</h1>", unsafe_allow_html=True)
    st.markdown("<a href='https://github.com/sameemul-haque/Video-to-Text' style='color: #6c7086; font-size: 0.9rem; text-align: center; position: fixed; bottom: 0; left: 0; text-decoration: none; border: solid 1px #6c7086; border-radius: 10px; padding: 0.5rem; margin: 1rem;'>Source Code</a>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload a video file here", type=["mp4"])

    if uploaded_file is not None:
        with st.spinner('Retreiving the text from the video. Please wait...'):
            extracted_audio = extract_audio(uploaded_file)
            model = whisper.load_model("base.en")
            result = model.transcribe(extracted_audio)
        st.markdown("***")
        st.subheader("Full text from the video")
        st.code(result["text"], language='None')
        st.markdown("***")
        st.subheader("Segments of text from the video")
        for segment in result["segments"]:
            st.code(segment["text"], language='None')
        st.markdown("***")

if __name__ == "__main__":
    main()
