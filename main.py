import ffmpeg
import whisper

input_video = "input.mp4"
input_video_name = input_video.replace(".mp4", "")

def extract_audio():
    extracted_audio = f"audio-{input_video_name}.wav"
    stream = ffmpeg.input(input_video)
    stream = ffmpeg.output(stream, extracted_audio)
    ffmpeg.run(stream, overwrite_output=True)
    return extracted_audio

def run():
    extracted_audio = extract_audio()
    model = whisper.load_model("base.en")
    result = model.transcribe(extracted_audio)
    print(result["text"])
run()