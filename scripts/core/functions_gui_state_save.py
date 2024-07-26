import os
import tempfile
import json

from scripts.core.classes import UiState

TEMP_DIR = tempfile.gettempdir()
FILE_NAME = "transcription_tool_ui_state.json"
UI_STATE_PATH = f"{TEMP_DIR}/{FILE_NAME}"


def save_ui_state(ui_state: UiState) -> None:
    """
    To retain the gui's state across different sessions, this will write a json
    that records the current state of the gui upon the window being closed.

    Args:
        ui_state: The state of the gui's widgets written to a UiState object.
    """
    ui_state_json_string = ui_state.as_json_string()

    with open(UI_STATE_PATH, "w") as file:
        file.write(ui_state_json_string)


def read_ui_state() -> UiState:
    """
    Intended to be run when a gui is opened to set the widgets to the
    previously set state.
    """
    if not os.path.exists(UI_STATE_PATH):
        return UiState() # returns empty UiState object

    with open(UI_STATE_PATH, "r") as file:
        ui_state_dict = json.loads(file.read())
        ui_state = UiState(
            mp3_path=ui_state_dict["mp3_path"],
            file_destination=ui_state_dict["file_destination"],
            model_type=ui_state_dict["model_type"],
            eng_only=ui_state_dict["eng_only"],
        )
    return ui_state


if __name__ == "__main__":
    ui = UiState(
        mp3_path="/home/ericnjkim/repo/transcription_tool/_mp3/mp3.mp3",
        file_destination="/home/ericnjkim/repo/transcription_tool/_exports",
        model_type="model_type_1",
        eng_only=True,
    )
    # save_ui_state(ui)
    print(read_ui_state())