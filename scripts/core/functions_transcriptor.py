
# import whisper
from datetime import datetime

def time_stamp() -> str:
    """ Returns the current time as a formatted string.
    Isolating the formatting of the date title string allows me to add in
    """
    datetime_today = datetime.now().date()
    datetime_date = '-'.join([str(datetime_today.day),
                              str(datetime_today.month),
                              str(datetime_today.year)])

    weekday_int = datetime.now().weekday()
    weekday_map = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
                   4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

    date_title = f"{weekday_map[weekday_int]} {datetime_date}"
    return date_title

# see if you can add option for writing out between md and txt
def create_file(
        dir_path: str,
        text: str,
        time_stamp: str,
        name: str = "Transcription") -> None:
    """
    Creates a file on disk to write the transcription text into.

    Args:
        dir_path: Directory to write file to.
        text: Transcription text to write into the file.
        time_stamp: Time stamp to write onto the file name.
        name: Base name of the write file.
    """
    file_ext = "txt"
    dir_path = dir_path.replace("\\", "/") # replace any backslashes
    file_path = f"{dir_path}/{name}_{time_stamp}.{file_ext}"

    with open(file_path, "w") as file:
        file.write(text)


def transcribe(mp3_path: str, model_type, time_stamp: str) -> str:
    """
    Takes input of mp3 file path and returns transcription provided by the whisper model.

    Args:
        mp3_path:
        model_type:
        time_stamp:
    """
    model = whisper.load_model(model_type)
    transcription = model.transcribe(mp3_path, fp16=False)

    return transcription

def run(mp3_path, model_type, dir_path) -> None:
    """ Conducts the execution of all functions in this module."""
    current_time_stamp = time_stamp()
    transcription = transcribe(
        mp3_path=mp3_path,
        model_type=model_type,
        time_stamp=current_time_stamp)
    create_file(
        dir_path=dir_path,
        text=transcription,
        time_stamp=current_time_stamp)

# test run for dev
if __name__ == "__main__":
    # run()
    create_file(r"\home\ericnjkim/repo/transcription_tool/_exports", "", "00-00")
