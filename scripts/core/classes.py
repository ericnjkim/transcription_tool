import json

from dataclasses import dataclass, asdict


@dataclass
class UiState:
    mp3_path: str = ""
    file_destination: str = ""
    model_type: str = ""
    eng_only: bool = True

    def as_dict(self) -> dict:
        return asdict(self)

    def as_json_string(self) -> str:
        ui_state_dict = self.as_dict()
        json_string = json.dumps(ui_state_dict, indent=4)
        return json_string



