
import whisper


def write_file(
        export_dir_path: str, text: str, name: str = "Transcription") -> None:
    """
    Creates a file on disk to write the transcription text into.

    Args:
        export_dir_path: Directory to write file to.
        text: Transcription text to write into the file.
        name: Base name of the write file.
    """
    export_dir_path = export_dir_path.replace("\\", "/")
    file_ext = "txt"
    file_path = f"{export_dir_path}/{name}.{file_ext}"

    with open(file_path, "w") as file:
        file.write(text)


def transcribe(audio_file_path: str, model_type: str) -> str:
    """
    Takes input of mp3 file path and returns transcription provided by the
    whisper model.

    Args:
        audio_file_path: The audio file to transcribe.
        model_type: The whisper ai model type to use including different sizes
        and whether to use an english only model.
    """
    # return f"testing some text"
    audio_file_path = audio_file_path.replace("\\", "/")
    model = whisper.load_model(model_type)
    transcription = model.transcribe(audio_file_path, fp16=False)["text"]
    # interprets the words "new line" as a prompt to break the text.
    transcription = transcription.replace(" new line", "\n")

    return transcription
