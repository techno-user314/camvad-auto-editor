# CamVAD Editor
CamVAD Editor performs automatic video editing of setups with multiple cameras and speakers.  
  
# Features
 - Edits multicam sequences with multiple speakers. Optimized for interview style recordings/scenarios.
 - Exports timeline to use in Adobe Premiere Pro, with or without the included UXP extension.
 - Chooses what camera angle is best for the cut based on voice detection and analysis.
 - Adjustable editing style.
 - Cuts are modifiable post processing.
 - Supports two-speaker setups, with one close-up cam for each person, plus a wide view. Requires each speaker to have their own mic/individual recording.

# User Guide
## What CamVAD Does
CamVAD needs an individual audio recording for both of the speakers in the video clip. Given the audio recordings, it generates a cut sequence of what shot to use (picking between close-up shots vs wide shots, and what person to focus on) based on who talks when. This sequence is then expired to Adobe Premier Pro, where you can choose to either use the included extension to automatically convert this into a video edit, or manually modify the sequence and do with it what you will.
## Setup
Follow the installation instructions to setup CamVAD on your PC.
## Quick Start
To create an edit:
 1. To to the "File Selection" page in the left navigation bar.  
 2. Drag each of your speakers' microphone recording audio files into the appropriate boxes on the page.  
 3. Specify when the program should start editing using the timestamp input fields on the right of each file upload box.
 4. Go to the final page of the navigation bar, "Create Edit", and select the button to start editing. The program will need a few minutes to process, depending on the length of the input.
 5. After processing finishes, CamVAD will create an XML file that can then be imported into Adobe Premier Pro. This XML  generates a sequence timeline with marked cut points. These markers are entirely adjustable.
 6. Import the XML into Premier.
 7. Add your videos to the timeline. Line up the video based on the audio file given to CamVAD to create the edit. The markers show where camera cuts are suggested.
### Optional Next Step
 8. Once the timeline is in Premier, and you have lined up your video tracks with the audio, open the extension that you installed with CamVAD.
 9. Press "Convert Markers".
## Other Settings in CamVAD
You will notice that there are other pages in the navigation bar.  
These are advanced settings, and it is recommended that you leave them at their default values. However, in some cases, adjusting these can create a better edit,  so they are provided for the adventurous user. Fair warning: They can take some experimentation to get right. Documentation is provided below:
# Installing CamVAD from a Release
## CamVAD Software
## Adobe Premier Extension
# Installing CamVAD from Source
## CamVAD Software
## Adobe Premier Extension


