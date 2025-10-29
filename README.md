# CamVAD Editor
CamVAD Editor performs automatic video editing of setups with multiple cameras and speakers.  

> [!WARNING] 
> This is the pre-release version. There may be breaking bugs, random crashes, etc.
  
Much of this program is still in minimal working version state. Much more polish, and more features coming soon!
  
# Features
 - Edits multicam sequences with multiple speakers. Optimized for interview style recordings/scenarios.
 - Exports sequences to use in Adobe Premiere Pro. (EDL files)
 - Chooses what camera angle is best for the cut based on voice detection and analysis.
 - Adjustable editing style.
 - Cuts are modifiable post processing.
 - Supports two-speaker setups, with one close-up cam for each person, plus a wide view. Requires each speaker to have their own mic/individual recording.

# User Guide
## What CamVAD Does
CamVAD needs an individual audio recording for both of the speakers in the video clip. Given the audio recordings, it generates a cut sequence of what shot to use (picking between close-up shots vs wide shots, and what person to focus on) based on who talks when. This sequence is then exported to Adobe Premiere Pro, where you can combine the camera shots to make a fully edited episode.
## Setup
Follow the [installation instructions](#installing-camvad) to setup CamVAD on your PC.
## Quick Start
Once CamVAD is open, to create an edit:
 1. Go to the "File Selection" page in the left navigation bar.  
 2. Drag each of your speakers' microphone recording audio files into the appropriate boxes on the page.  
 4. Go to the final page of the navigation bar, "Create Edit", and select the button to start editing. The program will need a few minutes to process, depending on the length of the input files.
 5. After processing finishes, CamVAD will create three EDL file that can then be imported into Adobe Premiere Pro.
 6. Import the EDLs into Premiere.
 7. In each EDL sequence, replace the source with the desired camera angle.
 8. Combine each sequence from the EDL files into a master sequence.
## Other Settings in CamVAD
***This feature is coming soon to the UI, for now, the extra settings are declared in Editor.__init__() of editor.py***  
You will notice that in the CamVAD UI, there are several extra pages included in the navigation bar.  
These give access to advanced settings, and it is recommended that you leave them at their default values. However, in some cases, adjusting these can create a better edit, so they are provided for the adventurous user. Fair warning: They can take some experimentation to get right. 
# Installing CamVAD
## From a Release
1. Download the zip for your operating system from the [releases page](https://github.com/techno-user314/camvad-editor/releases).
2. Unpack the zip file.
3. Navigate into the unpacked file and run the CamVAD executable.
## From Source
1. Set up a Python environment (Python version >3.13)
2. Install dependancies:
   - NumPy
   - Pandas
   - PyQt6
   - SoundFile
4. Download the source code
5. Unpack source, and run main.py
