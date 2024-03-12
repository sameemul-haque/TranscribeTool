import streamlit as st
import requests
from dotenv import load_dotenv
import os
import ffmpeg
from tempfile import NamedTemporaryFile
import yt_dlp

def process_file(input_file):
    output_file_name = f"{input_file}_processed.flac"
    ffmpeg.input(input_file).output(output_file_name, acodec='flac').run(overwrite_output=True)
    return output_file_name

def query(filename):
    API_URL = "https://api-inference.huggingface.co/models/openai/whisper-base.en"
    # locally
    HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    # cloud
    # HUGGINGFACEHUB_API_TOKEN = st.secrets["HUGGINGFACEHUB_API_TOKEN"]
    headers = {"Authorization": f"Bearer {HUGGINGFACEHUB_API_TOKEN}"}
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    if response.ok:
        return response.json()["text"]
    else:
        None

def main():
    st.set_page_config(
        page_title="TranscribeTool",
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
    load_dotenv()
    st.markdown("<h1 style='text-align: center; color: #a6e3a1;'>TranscribeTool</h1>", unsafe_allow_html=True)
    st.markdown("<a href='https://github.com/sameemul-haque/TranscribeTool' style='color: #6c7086; font-size: 1rem; text-align: center; position: fixed; top: 0; left: 0; text-decoration: none; border: solid 1px #6c7086; border-radius: 10px; padding: 0.5rem; margin: 1rem;'><img style='display: flex; justify-content: center; align-items: center; width: 1rem; filter: brightness(0) saturate(100%) invert(47%) sepia(12%) saturate(640%) hue-rotate(193deg) brightness(91%) contrast(86%);' src='https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/github/github-original.svg'/></a>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload a video file here")

    st.markdown(
    """
    <style>
    .separator {
    display: flex;
    align-items: center;
    text-align: center;
    color: #6c7086;
    }

    .separator::before,
    .separator::after {
    content: '';
    flex: 1;
    border-bottom: 1px dotted #6c7086;
    }

    .separator:not(:empty)::before {
    margin-right: .25em;
    }

    .separator:not(:empty)::after {
    margin-left: .25em;
    }
    </style>
    <div class="separator" data-testid="orSeperator">OR</div>
    """, 
    unsafe_allow_html=True)

    yturl = st.text_input("Type the URL of a youtube video here")
    ydl_opts = {
        'format': 'm4a/bestaudio/best',        
        'postprocessors': [{ 
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]
    }
    if (uploaded_file is not None and (uploaded_file.type.startswith('video/') or uploaded_file.type.startswith('audio/'))) or yturl:
        if uploaded_file:
            with st.spinner('Retrieving the text from the video. Please wait...'):
                with NamedTemporaryFile() as temp:
                    temp.write(uploaded_file.getvalue())
                    temp.seek(0)
                    processed_file = process_file(temp.name)
                    output = query(f"{processed_file}")
                st.markdown(
                """
                <style>
                [data-testid="stFileUploader"] {margin-bottom: -2.5rem !important;}
                </style>
                """
                , unsafe_allow_html=True)
        if yturl:
            st.markdown(
            """
            <style>
            [data-testid="stFileUploader"] {display: none !important;}
            [data-testid="orSeperator"] {display: none !important;}
            </style>
            """
            , unsafe_allow_html=True)
            with st.spinner('Downloading audio from URL. Please wait...'):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    try:
                        info_dict = ydl.extract_info(yturl, download=False)
                        ydl.download([yturl])
                        audio_file_path = ydl.prepare_filename(info_dict)[:-3] + "m4a"
                    except Exception as e:
                        st.error("An error occurred: " + "  \n  " + f"{e}")
                processed_file = audio_file_path
                output = query(f"{processed_file}")
        st.markdown("***")
        st.write(output)
        st.code(output, language="None")
        st.markdown("***")
        if processed_file is not None:
            os.remove(processed_file)
        
    else:
        if uploaded_file is not None:
            st.error("The file type is not supported")

if __name__ == "__main__":
    main()
