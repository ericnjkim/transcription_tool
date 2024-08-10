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

<img src="/_readme_images/transcription_tool_gui.png" alt="transcription_tool_gui" width="700"/>

### Directory contents:
Further docstrings can be found in modules.

- executables/: Compiled standalone exe to run the project and spec file to build
the exe.
- scripts/: working files for the tool.
  - scripts/core/: All logic for the working operation of the tool including use of the transcription model and any generic python library scripts.
  - scripts/qt/: All qt related scripts for tying the core scripts into the gui's widgets.
    - scripts/qt/qss/: Qt style sheet and icons for the gui.
    - scripts/qt/ui/: The ui files for the widget layout of the gui.

- scripts/core/classes.py: Stores any custom data classes used in the tools operation.
- scripts/core/functions_gui_state_save.py: Functions for the tools's gui state save feature.
- scripts/core/functions_transcriptor.py: Main working logic including use of the transcription model and the writing of files. 


### Using the tool:
The gui works in a two stage process. 
During the setup stage which is the gui's default state, you can set an input
file path, an export directory, options for the model type and whether the 
transcription should include non english languages.

Once these are populated, you will be able to transcribe a file. This will use
the open-ai whisper model to transcribe the audio file into text. The first time
this runs, it will also download the model for the specific settings so will be
slower.

After this completes, the text will be written into the transcription text
window. This allows you to check the transcription for any errors and to set
any breaks in the text manually before it's written out.

<img src="/_readme_images/transcription_mode.png" alt="transcription_tool_gui" width="700"/>

Once the text has been confirmed, the confirmation button will write the file
out to the export directory with a timestamp to prevent accidental overrides.

### Extra Behaviours
- Gui will remember its ui state upon closing so will self populate with the 
same settings the next time its run.
- To prevent file overrides, a timestamp is written on each transcription file.
- Depending on what is being done, either the setup or the transcription areas 
of the gui will be greyed out to prevent problems.
- Trying to transcribe without setting paths will be met with a dialog message 
error. 

### Challenges
- The transcribe function being called into the gui would freeze the gui as it
takes a while to complete its operation. To prevent a gui freeze, the 
transcription function is called onto a unique QThread before running.

### Future Goals
- Add options for file type to write out as.
- Add adjustable naming convention.
- Upon transcribing, add a loading circle.

### Credits

Qss style sheet base before modifications and qss icons: 
https://github.com/SZinedine/QBreeze


### WIP
- does it work with other audio files?