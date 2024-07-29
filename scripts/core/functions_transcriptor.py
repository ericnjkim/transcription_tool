
# import whisper

# see if you can add option for writing out between md and txt
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
        audio_file_path:
        model_type:
        time_stamp:
    """
    return f"testing some text"
    audio_file_path = audio_file_path.replace("\\", "/")
    model = whisper.load_model(model_type)
    transcription = model.transcribe(audio_file_path, fp16=False)
    # interprets the words "new line" as a prompt to break the text.
    transcription = transcription.replace(" new line", "\n")

    return f"{time_stamp}\n\n{transcription}"

# test run for dev
if __name__ == "__main__":
    pass
    # run(audio_file_path=r"\home\ericnjkim/repo/transcription_tool/_mp3/2023_05_01.mp3",
    #     model_type="tiny",
    #     export_dir_path=r"\home\ericnjkim/repo/transcription_tool/_exports",)
    # create_file(r"\home\ericnjkim/repo/transcription_tool/_exports", "", "00-00")
