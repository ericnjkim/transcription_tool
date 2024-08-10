## Transcription Tool

### Project description:
This gui tool takes a mp3 file and transcribes it into text to be written out 
as its own file. 

It uses the open-ai whisper model to transcribe audio files into text and this
gui tool acts as a wrapper around that model to make it easier to transcribe and 
write files out. 

I initially made this as a way to make my daily diary writing a bit easier, 
but I found I'm fairly awful when it comes to reciting what's happened in the 
day on the spot. It still was an enjoyable project and allowed me to review and 
use some skill's and tools I had previously learnt.


### Directory contents:
- bin: Executable files to run the gui tool.
- scripts: working files for the tool.
  - scripts/core: All logic for the working operation of the tool including use of the transcription model and any generic python library scripts.
    - scripts/core/classes.py: Stores any custom data classes used in the tools operation.
    - scripts/core/functions_gui_state_save.py: Functions for the tools's gui state save feature.
    - scripts/core/functions_transcriptor.py: Main working logic including use of the transcription model and the writing of files. 
  - scripts/qt: All qt related scripts for tying the core scripts into the gui's widgets.
    - scripts/qt/transcriptor_main.py:
  - scripts/run.py: Target point for the executable files to run the gui from.   


### Using the tool:
The gui works in a two stage process. 
During the setup stage which is the gui's default state, you can set an input
file path, an export directory, options for the model type and whether the 
transcription should include non english languages.

Once these are populated, you will be able to transcribe a file. This will use
the open-ai whisper model to transcribe the audio file into text.

After this completes, the text will be written into the transcription text
window. This allows you to check the transcription for any errors and to set
any breaks in the text manually before it's written out.

Once the text has been confirmed, the confirmation button will write the file
out to the export directory with a timestamp to prevent accidental overrides.


### WIP
restrict transcription without having set paths
download local model whisper