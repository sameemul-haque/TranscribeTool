# VideoTool

This project is a simple tool that allows users to upload a video or audio file and extract text from it. It utilizes [Streamlit](https://streamlit.io/) for the user interface and [ffmpeg](https://ffmpeg.org/) for audio extraction, [Whisper](https://openai.com/research/whisper) library for speech recognition, and [yt-dlp](https://github.com/yt-dlp/yt-dlp) for retrieving audio from a video url.

- Report issues [here](https://github.com/sameemul-haque/VideoTool/issues/new?labels=bug&projects=&template=bug_report.md&title=%5Bbug%5D) 
- Request features [here](https://github.com/sameemul-haque/VideoTool/issues/new?labels=enhancement&projects=&template=feature_request.md&title=%5Bfeat%5D)

## Usage

1. Open https://videotool.streamlit.app/
2. Upload a video | audio file or provide url of a video.
3. Wait for the transcription process to complete.
4. View the full text extracted from the file and its segmented text.


## Installation

To run this project locally, follow these steps:

1. Clone this repository to your local machine.
2. Navigate to the project directory.
3. Create and activate a virtual environment (optional but recommended):
```
python3 -m venv venv
source venv/bin/activate
```
4. Install the required dependencies using pip:
```
pip install -r requirements.txt
```

5. Run the following command to start the Streamlit app:

```
streamlit run main.py 
```

6. Open your web browser and go to the URL provided by Streamlit.
7. Upload a video | audio file or provide url of a video.
8. Wait for the transcription process to complete.
9. View the full text extracted from the file and its segmented text.

## Acknowledgements

This project uses the following libraries:

- [ffmpeg-python](https://github.com/kkroening/ffmpeg-python) for audio extraction.
- [Streamlit](https://github.com/streamlit/streamlit) for building the web application.
- [Whisper](https://github.com/openai/whisper) for speech recognition.
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for retrieving audio from a video url.

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.


<!-- 
streamlit==1.31.1
ffmpeg-python==0.2.0
openai-whisper==20231117
yt-dlp==2023.12.30
-->