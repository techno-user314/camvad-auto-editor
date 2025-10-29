import os
import soundfile as sf

from audio_processing import *

def get_cuts_from_frames(frames):
    """
    Convert a list of camera frames into a list of cuts.
    """
    if not frames:
        return []

    cuts = []
    start_index = 0
    current_cam = frames[0]

    for i in range(1, len(frames)):
        if frames[i] != current_cam:
            duration = i - start_index
            match current_cam:
                case Cam.C1:
                    cam_name = "Close-up 1"
                case Cam.C2:
                    cam_name = "Close-up 2"
                case Cam.WIDE:
                    cam_name = "Wide"
            cuts.append((start_index, duration, cam_name))
            start_index = i
            current_cam = frames[i]

    # Add the final cut
    duration = len(frames) - start_index
    cuts.append((start_index, duration, cam_name))
    return cuts

class Editor:
    def __init__(self, data):
        self.frame_ms = 30
        self.fps = 30
        self.energy_threshold = 0.015  # Threshold to activate talk mode
        self.dominance_ratio = 2.0  # Audio bleed filtering

        self.silence_min_time = 1  # Number of seconds a speaker is silent to end their focus

        self.cam1_min_talk_time = 1  # Number of seconds cam 1 talking has to be to get focus
        self.cam2_min_talk_time = 0.5  # Number of seconds cam 2 talking has to be to get focus

        self.close_cam_reward = 5
        self.wide_reward = 4
        self.miss_speaker_penalty = 5
        self.cut_splits = [15, 35]
        self.cut_penalties = [60, 35, 2]

        self.audio_file1 = None
        self.audio_file2 = None
        self.sample_rate = None

        self.cam_frames = None

    def load_audio(self, path1, path2):
        self.audio_file1, sr1 = sf.read(path1)
        self.audio_file2, sr2 = sf.read(path2)
        assert sr1 == sr2
        self.sample_rate = sr1

    def process_audio(self):
        # === CONVERT TO MONO, NORMALIZE, AND SYNC ===
        audio1 = self.audio_file1
        audio2 = self.audio_file2
        if audio1.ndim > 1:
            audio1 = np.mean(audio1, axis=1)
        if audio2.ndim > 1:
            audio2 = np.mean(audio2, axis=1)

        audio1 = normalize_audio(audio1)
        audio2 = normalize_audio(audio2)

        # Sync lengths
        min_len = min(len(audio1), len(audio2))
        audio1 = audio1[:min_len]
        audio2 = audio2[:min_len]

        frame_len = int(self.sample_rate * self.frame_ms / 1000)

        # === PREPROCESS PASS 1 - Speaker Activity ===
        speaker1_active, speaker2_active = voice_detect(audio1, audio2,
                                                        min_len, frame_len,
                                                        self.energy_threshold,
                                                        self.dominance_ratio)

        # === PREPROCESS PASS 2 - Smoothing ===
        speaker1_active = lookahead_smoothing(speaker1_active, self.silence_min_time)
        speaker2_active = lookahead_smoothing(speaker2_active, self.silence_min_time)

        speaker1_active = label_injections(speaker1_active, self.cam1_min_talk_time)
        speaker2_active = label_injections(speaker2_active, self.cam2_min_talk_time)

        # === PROCESSING - Optimal Cutting ===
        frames = list(zip(speaker1_active, speaker2_active))
        score, _, cf = dp_edit(frames,
                                self.close_cam_reward,
                                self.wide_reward,
                                self.miss_speaker_penalty,
                                self.cut_splits,
                                self.cut_penalties,
                                stride=5, max_l=300
        )
        self.cam_frames = cf

    def export_cuts(self, output_dir="."):
        """
        Export an EDL file for each camera based on the list of cuts.

        Parameters:
        - output_dir: Directory to save the EDL files
        """
        cuts = get_cuts_from_frames(self.cam_frames)

        # Group cuts by camera name
        cams = {}
        for start, duration, cam in cuts:
            cams.setdefault(cam, []).append((start, duration))

        def frames_to_timecode(frame):
            total_seconds = frame / self.fps
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            seconds = int(total_seconds % 60)
            frames = int(round((total_seconds - int(total_seconds)) * self.fps))
            return f"{hours:02}:{minutes:02}:{seconds:02}:{frames:02}"

        for cam_name, cam_cuts in cams.items():
            edl_lines = []
            edl_lines.append(f"TITLE: Sequence - {cam_name}")
            edl_lines.append("FCM: NON-DROP FRAME\n")

            for i, (start_frame, duration) in enumerate(cam_cuts, start=1):
                video_in = frames_to_timecode(start_frame)
                video_out = frames_to_timecode(start_frame + duration - 1)

                edit_num = f"{i:03}"
                reel_name = "AX"
                track = "V"
                transition = "C"

                edl_lines.append(
                    f"{edit_num}  {reel_name:<8} {track:<2} {transition:<2}  "
                    f"{video_in} {video_out} {video_in} {video_out}"
                )
                edl_lines.append(f"* FROM CLIP NAME: {cam_name}\n")

            # Write the EDL file for this camera
            filename = f"Sequence_{cam_name.replace(' ', '_')}.edl"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, "w") as f:
                f.write("\n".join(edl_lines))

#edittest = Editor(None)
#edittest.load_audio("./audio_cam1.wav", "./audio_cam2.wav")
#edittest.process_audio()
#edittest.export_cuts_test()
