# CamVAD Editor
CamVAD Editor assists with video editing for setups with multiple cameras and people speaking.  
  
# Features
 - Edits multicam sequences with multiple speakers. Optimized for interview style recordings/scenarios.
 - Exports timeline to use in Adobe Premiere Pro, with or without the included UXP extension.
 - Chooses what camera angle is best for the cut based on voice detection and analysis.
 - Adjustable editing style.
 - Cuts are modifiable post processing.
 - Supports two-speaker setups, with one close-up cam for each person, plus a wide view. Requires each speaker to have their own mic/individual recording.

# User Guide
## What CamVAD Does
CamVAD needs an individual audio recording for both of the speakers in the video clip. Given the audio recordings, it generates a cut sequence of what shot to use (picking between close-up shots vs wide shots, and what person to focus on) based on who talks when. This sequence is then exported to Adobe Premiere Pro, where you can choose to either use the included extension to automatically convert this into a video edit, or manually modify the sequence and do with it what you will.
## Setup
Follow the installation instructions to setup CamVAD on your PC.
## Quick Start
Once CamVAD is open, to create an edit:
 1. Go to the "File Selection" page in the left navigation bar.  
 2. Drag each of your speakers' microphone recording audio files into the appropriate boxes on the page.  
 4. Go to the final page of the navigation bar, "Create Edit", and select the button to start editing. The program will need a few minutes to process, depending on the length of the input files.
 5. After processing finishes, CamVAD will create an XML file that can then be imported into Adobe Premiere Pro. This XML  generates a sequence timeline with marked cut points. These markers are entirely adjustable.
 6. Import the XML into Premiere.
 7. Add your videos (from all camera angles) to the timeline. Line up the videos to the audio in the timeline. Once the videos are lined up, the markers show where camera changes are suggested.
### Optional Next Step
The extension included in this repository makes it possible to have the markers automatically converted to camera cuts. To do this: 
 1. Once all the camera clips are lined up with the markers in the timeline, nest them.
 2. Open the CamVAD Premiere extension.
 3. Click the button to convert markers to cuts.
 4. All the camera changes suggested by CanVAD will be applied to create a video ready to be exported.
## Other Settings in CamVAD
You will notice that in the CamVAD UI, there are several extra pages included in the navigation bar.  
These give access to advanced settings, and it is recommended that you leave them at their default values. However, in some cases, adjusting these can create a better edit, so they are provided for the adventurous user. Fair warning: They can take some experimentation to get right. 
# Installing CamVAD from a Release
## CamVAD Software
## Adobe Premiere Extension
# Installing CamVAD from Source
## CamVAD Software
## Adobe Premiere Extension
