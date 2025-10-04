import numpy as np

FRAME_MS = 30

class Cam:
    WIDE = 3
    C1 = 1
    C2 = 2

# === VOICE DETECTION AND PROCESSING ===
def voice_detect(speaker1_audio, speaker2_audio, min_len, frame_len,
                 threshold, dominance):
    def rms(frame):
        return np.sqrt(np.mean(np.square(frame)) + 1e-9)

    speaker1_active = []
    speaker2_active = []
    for i in range(0, min_len, frame_len):
        f1 = speaker1_audio[i:i + frame_len]
        f2 = speaker2_audio[i:i + frame_len]

        e1, e2 = rms(f1), rms(f2)

        s1 = s2 = 0
        if e1 > threshold or e2 > threshold:
            if e1 > e2 * dominance:
                s1 = 1
            elif e2 > e1 * dominance:
                s2 = 1
            else:
                s1 = s2 = 1

        speaker1_active.append(s1)
        speaker2_active.append(s2)

    return speaker1_active, speaker2_active

def lookahead_smoothing(activity, lookahead_time):
    lookahead_time = int(lookahead_time * 1000 / FRAME_MS)
    smoothed = activity.copy()
    length = len(activity)

    for i in range(length):
        if activity[i] == 0 and smoothed[i-1] != 0:
            # Look ahead to see if it's really the end
            end = min(i + lookahead_time, length)
            if np.any(activity[i+1:end]):
                smoothed[i] = 1  # Treat as part of ongoing speech
    return smoothed

def label_injections(speaker_activity, min_talk_time_sec):
    min_talk_frames = int(min_talk_time_sec * 1000 / FRAME_MS)
    labeled = speaker_activity.copy()
    length = len(speaker_activity)

    i = 0
    while i < length:
        if speaker_activity[i] == 1:
            start = i
            while i < length and speaker_activity[i] == 1:
                i += 1
            end = i
            burst_length = end - start
            if burst_length < min_talk_frames:
                for j in range(start, end):
                    labeled[j] = 0.5
        else:
            i += 1

    return labeled

# === CUT LABELING ===
def score_frame(cam, s1, s2, closeup_reward, wide_reward, miss_penalty):
    """Per-frame reward/penalty for a chosen camera."""
    if cam == Cam.C1:
        return (closeup_reward if s1 else 0) + (-miss_penalty if s2 else 0)
    elif cam == Cam.C2:
        return (closeup_reward if s2 else 0) + (-miss_penalty if s1 else 0)
    elif cam == Cam.WIDE:
        return wide_reward if (s1 or s2) else 0

def cut_penalty(frames_since_last_cut, cut_splits, cut_penalties):
    """Nonlinear cut penalty"""
    for cut_time, penalty in zip(cut_splits, cut_penalties):
        if frames_since_last_cut < cut_time:
            return penalty
    return cut_penalties[-1]

def dp_edit(frames,
            close_cam_reward, wide_reward, miss_speaker_penalty,
            cut_splits, cut_penalties,
            stride=5, max_l=300):
    """
    DP for optimal edit sequence with nonlinear cut penalty.
    frames: list of (s1, s2, sentence_break) -- sentence_break ignored here
    stride: how many frames to skip between DP steps (downsampling)
    max_l: maximum "frames since last cut" tracked
    Returns: (best_score, compressed_seq, expanded_seq)
    """
    # Downsample input frames
    frames_ds = frames[::stride]
    n = len(frames_ds)
    cams = [Cam.WIDE, Cam.C1, Cam.C2]

    # Two rolling DP layers
    prev_dp = [[-float('inf')] * (max_l+1) for _ in cams]
    curr_dp = [[-float('inf')] * (max_l+1) for _ in cams]

    # Backpointer storage
    back = [[[-1] * (max_l+1) for _ in cams] for _ in range(n)]

    # Init first frame
    s1, s2 = frames_ds[0]
    for ci, cam in enumerate(cams):
        prev_dp[ci][0] = score_frame(cam, s1, s2,
                                     close_cam_reward, wide_reward,
                                     miss_speaker_penalty)

    # Fill DP
    for t in range(1, n):
        s1, s2 = frames_ds[t]
        frame_score = [score_frame(cam, s1, s2,
                                   close_cam_reward, wide_reward,
                                   miss_speaker_penalty) for cam in cams]

        # Reset current layer
        for ci in range(len(cams)):
            for l in range(max_l+1):
                curr_dp[ci][l] = -float('inf')

        for ci, cam in enumerate(cams):
            for pj, prev_cam in enumerate(cams):
                for l_prev, prev_score in enumerate(prev_dp[pj]):
                    if prev_score == -float('inf'):
                        continue

                    if cam == prev_cam:
                        l_new = min(l_prev+1, max_l)
                        cand = prev_score + frame_score[ci]
                    else:
                        penalty = cut_penalty(l_prev, cut_splits, cut_penalties)
                        l_new = 0
                        cand = prev_score + frame_score[ci] - penalty

                    if cand > curr_dp[ci][l_new]:
                        curr_dp[ci][l_new] = cand
                        back[t][ci][l_new] = (pj, l_prev)

        # Roll layers forward
        prev_dp, curr_dp = curr_dp, prev_dp

    # Backtrack
    best_val = -float('inf')
    best_state = None
    for ci in range(len(cams)):
        for l in range(max_l+1):
            if prev_dp[ci][l] > best_val:
                best_val = prev_dp[ci][l]
                best_state = (ci, l)

    seq = []
    t = n-1
    ci, l = best_state
    while t >= 0:
        seq.append(cams[ci])
        prev = back[t][ci][l]
        if prev == -1 or prev is None:
            break
        ci, l = prev
        t -= 1

    seq.reverse()  # compressed sequence

    # Expand back to full frame length
    expanded = []
    for cam in seq:
        expanded.extend([cam] * stride)
    # Adjust length in case frames not divisible by stride
    expanded = expanded[:len(frames)]

    return best_val, seq, expanded