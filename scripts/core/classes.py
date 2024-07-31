import json
import os
from dataclasses import dataclass, asdict


@dataclass
class UiState:
    audio_file_path: str = ""
    export_dir_path: str = ""
    model_type: str = ""
    eng_only: bool = True

    def as_dict(self) -> dict:
        return asdict(self)

    def as_json_string(self) -> str:
        ui_state_dict = self.as_dict()
        json_string = json.dumps(ui_state_dict, indent=4)
        return json_string

    def check_parameters_valid(self) -> bool:
        """ To be used to check if enough parameters had been filled and path's
        are valid to allow the transcription operation to begin.
        """
        validity = (self.audio_file_path
        and self.export_dir_path
        and os.path.exists(self.audio_file_path)
        and os.path.exists(self.export_dir_path))
        return validity




