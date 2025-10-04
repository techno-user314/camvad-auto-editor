import soundfile as sf
import xml.etree.ElementTree as ET

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
            #cuts.append((start_index, duration, current_cam))
            cuts.append(start_index)
            start_index = i
            current_cam = frames[i]

    # Add the final cut
    duration = len(frames) - start_index
    #cuts.append((start_index, duration, current_cam.value))
    cuts.append(start_index)
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
        # === CONVERT TO MONO AND SYNC ===
        if self.audio_file1.ndim > 1:
            audio1 = np.mean(self.audio_file1, axis=1)
        else:
            audio1 = self.audio_file1
        if self.audio_file2.ndim > 1:
            audio2 = np.mean(self.audio_file2, axis=1)
        else:
            audio2 = self.audio_file2

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

    def export_cuts(self, width = 1920, height = 1080):
        # === EXPORT STEP 1 - Create a Cut List ===
        cuts = get_cuts_from_frames(self.cam_frames)

        # === EXPORT STEP 2 - Save Cuts as XML File ===
        def make_elem(tag, text=None, attrib=None):
            el = ET.Element(tag)
            if text is not None:
                el.text = str(text)
            if attrib:
                el.attrib = attrib
            return el

        xmeml = ET.Element("xmeml", version="5")

        # <sequence>
        sequence = make_elem("sequence", attrib={"id": "sequence-1"})
        xmeml.append(sequence)

        sequence.append(make_elem("name", "CamVAD Exported Cut List"))
        sequence.append(make_elem("duration", str(max(cuts) + 100)))

        # <rate>
        rate = make_elem("rate")
        rate.append(make_elem("timebase", self.fps))
        rate.append(make_elem("ntsc", "FALSE"))
        sequence.append(rate)

        # <media>
        media = make_elem("media")
        sequence.append(media)

        # <media><video>
        video = make_elem("video")
        media.append(video)

        format_el = make_elem("format")
        video.append(format_el)

        sample_char = make_elem("samplecharacteristics")
        format_el.append(sample_char)

        rate_el = make_elem("rate")
        rate_el.append(make_elem("timebase", self.fps))
        rate_el.append(make_elem("ntsc", "FALSE"))
        sample_char.append(rate_el)

        sample_char.append(make_elem("width", width))
        sample_char.append(make_elem("height", height))
        sample_char.append(make_elem("anamorphic", "FALSE"))
        sample_char.append(make_elem("pixelaspectratio", "square"))
        sample_char.append(make_elem("fielddominance", "none"))

        video.append(make_elem("track"))  # empty track

        # <media><audio>
        audio = make_elem("audio")
        media.append(audio)

        audio_format = make_elem("format")
        audio.append(audio_format)

        audio_sample_char = make_elem("samplecharacteristics")
        audio_format.append(audio_sample_char)

        audio_sample_char.append(make_elem("depth", "16"))
        audio_sample_char.append(make_elem("samplerate", "48000"))

        audio.append(make_elem("track"))  # empty track

        # <markers>
        markers = make_elem("markers")
        sequence.append(markers)

        for i, frame in enumerate(cuts, start=1):
            marker = make_elem("marker")
            marker.append(make_elem("comment", f"Marker {i}"))
            marker.append(make_elem("in", str(frame)))
            marker.append(make_elem("out", str(frame)))
            marker.append(make_elem("name", f"Marker {i}"))
            marker.append(make_elem("color", "Red"))
            markers.append(marker)

        # Write to file
        tree = ET.ElementTree(xmeml)
        ET.indent(tree, space="  ", level=0)  # Python 3.9+
        tree.write("premiere_markers.xml", encoding="utf-8", xml_declaration=True)
        print("XML file 'premiere_markers.xml' created successfully.")


#edittest = Editor(None)
#edittest.load_audio("./cam1.wav", "./cam2.wav")
#edittest.process_audio()
#edittest.export_cuts()