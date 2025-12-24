#!/usr/bin/env python3
"""
Terminal Christmas Tree Animation - Version A (Classic Blinking)
Features: Blinking ornaments, pulsing star, colored decorations
"""

import os
import random
import shutil  # For getting terminal size
import subprocess
import sys
import tempfile
import threading
import time
import wave
from array import array

# ANSI Color codes
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def clear_screen():
    """Clear the terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')


# --- Chiptune soundtrack helpers -------------------------------------------------

CHRISTMAS_TREE_NO_AUDIO = "CHRISTMAS_TREE_NO_AUDIO"
NO_MUSIC_FLAGS = {"--no-music", "--mute"}
CHIPTUNE_BPM = 80  # Extracted from the reference MIDI (BitMidi upload 35211)
SAMPLE_RATE = 22050  # Lower sample rate keeps the square wave authentic

# Polyphonic note events from the BitMidi reference (melody, harmony, bass)
CHIPTUNE_EVENTS = [
    (0.0, 0.5, 'C4'),
    (0.5, 0.75, 'A3'),
    (0.5, 0.75, 'F4'),
    (0.5, 1.0, 'F2'),
    (1.25, 0.25, 'A3'),
    (1.25, 0.25, 'F4'),
    (1.5, 1.0, 'A2'),
    (1.5, 1.5, 'C4'),
    (1.5, 1.5, 'F4'),
    (2.5, 1.0, 'C3'),
    (3.0, 0.5, 'E4'),
    (3.0, 0.5, 'G4'),
    (3.5, 0.75, 'F4'),
    (3.5, 0.75, 'A4'),
    (3.5, 1.0, 'F3'),
    (4.25, 0.25, 'F4'),
    (4.25, 0.25, 'A4'),
    (4.5, 1.0, 'F2'),
    (4.5, 1.5, 'F4'),
    (4.5, 1.5, 'A4'),
    (5.5, 1.0, 'F3'),
    (6.0, 0.5, 'C4'),
    (6.0, 0.5, 'A4'),
    (6.5, 0.5, 'A#2'),
    (6.5, 0.5, 'D4'),
    (6.5, 0.5, 'G4'),
    (7.0, 0.5, 'A2'),
    (7.0, 0.5, 'C4'),
    (7.0, 0.5, 'A4'),
    (7.5, 1.0, 'G2'),
    (7.5, 1.0, 'A#3'),
    (7.5, 1.0, 'A#4'),
    (8.5, 1.0, 'C3'),
    (8.5, 1.0, 'A#3'),
    (8.5, 1.0, 'E4'),
    (9.5, 1.0, 'A#3'),
    (9.5, 1.0, 'G4'),
    (9.5, 2.0, 'F2'),
    (10.5, 1.0, 'A3'),
    (10.5, 1.0, 'F4'),
    (11.5, 1.0, 'F3'),
    (12.0, 0.5, 'C5'),
    (12.5, 0.5, 'A3'),
    (12.5, 0.5, 'C5'),
    (12.5, 1.0, 'F4'),
    (13.0, 0.5, 'F3'),
    (13.0, 0.5, 'A4'),
    (13.5, 1.5, 'A#3'),
    (13.5, 1.5, 'D5'),
    (13.5, 2.0, 'F4'),
    (15.0, 0.5, 'A3'),
    (15.0, 0.5, 'C5'),
    (15.5, 0.75, 'C5'),
    (15.5, 2.0, 'G3'),
    (15.5, 3.0, 'D4'),
    (16.25, 0.25, 'A#4'),
    (16.5, 1.5, 'A#4'),
    (17.5, 1.0, 'F3'),
    (18.0, 0.5, 'A#4'),
    (18.5, 0.5, 'A#4'),
    (18.5, 1.5, 'E3'),
    (18.5, 1.5, 'C4'),
    (19.0, 0.5, 'G4'),
    (19.5, 1.5, 'C5'),
    (20.0, 0.5, 'C3'),
    (20.0, 0.5, 'E4'),
    (20.5, 0.5, 'D3'),
    (20.5, 0.5, 'F4'),
    (21.0, 0.5, 'E3'),
    (21.0, 0.5, 'G4'),
    (21.0, 0.5, 'A#4'),
    (21.5, 0.75, 'G4'),
    (21.5, 0.75, 'A#4'),
    (21.5, 2.0, 'F3'),
    (22.25, 0.25, 'F4'),
    (22.25, 0.25, 'A4'),
    (22.5, 1.0, 'F4'),
    (22.5, 1.0, 'A4'),
    (24.0, 0.5, 'C4'),
    (24.5, 0.75, 'F4'),
    (24.5, 1.0, 'F2'),
    (24.5, 1.0, 'A3'),
    (25.25, 0.25, 'F4'),
    (25.5, 1.0, 'A2'),
    (25.5, 1.5, 'C4'),
    (25.5, 1.5, 'F4'),
    (26.5, 1.0, 'C3'),
    (27.0, 0.5, 'E4'),
    (27.0, 0.5, 'G4'),
    (27.5, 0.75, 'F4'),
    (27.5, 0.75, 'A4'),
    (27.5, 2.0, 'F3'),
    (28.25, 0.25, 'F4'),
    (28.25, 0.25, 'A4'),
    (28.5, 1.5, 'F4'),
    (28.5, 1.5, 'A4'),
    (29.5, 1.0, 'F2'),
    (30.0, 0.5, 'C4'),
    (30.0, 0.5, 'A4'),
    (30.5, 0.5, 'A#2'),
    (30.5, 0.5, 'D4'),
    (30.5, 0.5, 'G4'),
    (31.0, 0.5, 'A2'),
    (31.0, 0.5, 'C4'),
    (31.0, 0.5, 'A4'),
    (31.5, 1.0, 'G2'),
    (31.5, 1.0, 'D4'),
    (31.5, 1.0, 'A#4'),
    (32.5, 1.0, 'C3'),
    (32.5, 1.0, 'A#3'),
    (32.5, 1.0, 'E4'),
    (33.5, 1.0, 'A#3'),
    (33.5, 1.0, 'G4'),
    (33.5, 2.0, 'F2'),
    (34.5, 1.0, 'A3'),
    (34.5, 1.0, 'F4'),
    (36.0, 0.5, 'C4'),
    (36.5, 0.75, 'A3'),
    (36.5, 0.75, 'F4'),
    (36.5, 1.0, 'F2'),
    (37.25, 0.25, 'A3'),
    (37.25, 0.25, 'F4'),
    (37.5, 1.0, 'A2'),
    (37.5, 1.5, 'C4'),
    (37.5, 1.5, 'F4'),
    (38.5, 1.0, 'C3'),
    (39.0, 0.5, 'E4'),
    (39.0, 0.5, 'G4'),
    (39.5, 0.75, 'F4'),
    (39.5, 0.75, 'A4'),
    (39.5, 1.0, 'F3'),
    (40.25, 0.25, 'F4'),
    (40.25, 0.25, 'A4'),
    (40.5, 1.0, 'F2'),
    (40.5, 1.5, 'F4'),
    (40.5, 1.5, 'A4'),
    (41.5, 1.0, 'F3'),
    (42.0, 0.5, 'C4'),
    (42.0, 0.5, 'A4'),
    (42.5, 0.5, 'A#2'),
    (42.5, 0.5, 'D4'),
    (42.5, 0.5, 'G4'),
    (43.0, 0.5, 'A2'),
    (43.0, 0.5, 'C4'),
    (43.0, 0.5, 'A4'),
    (43.5, 1.0, 'G2'),
    (43.5, 1.0, 'A#3'),
    (43.5, 1.0, 'A#4'),
    (44.5, 1.0, 'C3'),
    (44.5, 1.0, 'A#3'),
    (44.5, 1.0, 'E4'),
    (45.5, 1.0, 'A#3'),
    (45.5, 1.0, 'G4'),
    (45.5, 2.0, 'F2'),
    (46.5, 1.0, 'A3'),
    (46.5, 1.0, 'F4'),
    (47.5, 1.0, 'F3'),
    (48.0, 0.5, 'C5'),
    (48.5, 0.5, 'A3'),
    (48.5, 0.5, 'C5'),
    (48.5, 1.0, 'F4'),
    (49.0, 0.5, 'F3'),
    (49.0, 0.5, 'A4'),
    (49.5, 1.5, 'A#3'),
    (49.5, 1.5, 'D5'),
    (49.5, 2.0, 'F4'),
    (51.0, 0.5, 'A3'),
    (51.0, 0.5, 'C5'),
    (51.5, 0.75, 'C5'),
    (51.5, 2.0, 'G3'),
    (51.5, 3.0, 'D4'),
    (52.25, 0.25, 'A#4'),
    (52.5, 1.5, 'A#4'),
    (53.5, 1.0, 'F3'),
    (54.0, 0.5, 'A#4'),
    (54.5, 0.5, 'A#4'),
    (54.5, 1.5, 'E3'),
    (54.5, 1.5, 'C4'),
    (55.0, 0.5, 'G4'),
    (55.5, 1.5, 'C5'),
    (56.0, 0.5, 'C3'),
    (56.0, 0.5, 'E4'),
    (56.5, 0.5, 'D3'),
    (56.5, 0.5, 'F4'),
    (57.0, 0.5, 'E3'),
    (57.0, 0.5, 'G4'),
    (57.0, 0.5, 'A#4'),
    (57.5, 0.75, 'G4'),
    (57.5, 0.75, 'A#4'),
    (57.5, 2.0, 'F3'),
    (58.25, 0.25, 'F4'),
    (58.25, 0.25, 'A4'),
    (58.5, 1.0, 'F4'),
    (58.5, 1.0, 'A4'),
    (60.0, 0.5, 'C4'),
    (60.5, 0.75, 'F4'),
    (60.5, 1.0, 'F2'),
    (60.5, 1.0, 'A3'),
    (61.25, 0.25, 'F4'),
    (61.5, 1.0, 'A2'),
    (61.5, 1.5, 'C4'),
    (61.5, 1.5, 'F4'),
    (62.5, 1.0, 'C3'),
    (63.0, 0.5, 'E4'),
    (63.0, 0.5, 'G4'),
    (63.5, 0.75, 'F4'),
    (63.5, 0.75, 'A4'),
    (63.5, 2.0, 'F3'),
    (64.25, 0.25, 'F4'),
    (64.25, 0.25, 'A4'),
    (64.5, 1.5, 'F4'),
    (64.5, 1.5, 'A4'),
    (65.5, 1.0, 'F2'),
    (66.0, 0.5, 'C4'),
    (66.0, 0.5, 'A4'),
    (66.5, 0.5, 'A#2'),
    (66.5, 0.5, 'D4'),
    (66.5, 0.5, 'G4'),
    (67.0, 0.5, 'A2'),
    (67.0, 0.5, 'C4'),
    (67.0, 0.5, 'A4'),
    (67.5, 1.0, 'G2'),
    (67.5, 1.0, 'D4'),
    (67.5, 1.0, 'A#4'),
    (68.5, 1.0, 'C3'),
    (68.5, 1.0, 'A#3'),
    (68.5, 1.0, 'E4'),
    (69.5, 1.0, 'A#3'),
    (69.5, 1.0, 'G4'),
    (69.5, 2.0, 'F2'),
    (70.5, 1.0, 'A3'),
    (70.5, 1.0, 'F4'),
]

NOTE_OFFSETS = {
    'C': -9,
    'C#': -8,
    'Db': -8,
    'D': -7,
    'D#': -6,
    'Eb': -6,
    'E': -5,
    'F': -4,
    'F#': -3,
    'Gb': -3,
    'G': -2,
    'G#': -1,
    'Ab': -1,
    'A': 0,
    'A#': 1,
    'Bb': 1,
    'B': 2,
}


def note_to_frequency(note):
    """Convert note name (e.g., 'A4') to frequency in Hz."""
    if not note or note.upper() == 'REST':
        return None

    note = note.strip().replace('♯', '#').replace('♭', 'b')
    octave = int(note[-1])
    pitch = note[:-1]
    pitch = pitch[0].upper() + pitch[1:]
    if pitch not in NOTE_OFFSETS:
        raise ValueError(f"Unsupported note: {note}")

    semitone_offset = NOTE_OFFSETS[pitch] + (octave - 4) * 12
    return 440.0 * (2 ** (semitone_offset / 12.0))


def amplitude_for_note(note_name):
    """Return a register-aware amplitude to keep the mix balanced."""
    octave = int(note_name[-1])
    if octave <= 2:
        return 4500
    if octave == 3:
        return 6500
    if octave == 4:
        return 8500
    return 9500


def render_polyphonic_events(events, bpm, sample_rate, duty_cycle=0.5):
    """Render all MIDI-derived note events directly into a PCM buffer."""
    if not events:
        return array('h')

    seconds_per_beat = 60.0 / bpm
    total_beats = max(start + duration for start, duration, _ in events)
    total_frames = int(total_beats * seconds_per_beat * sample_rate) + sample_rate
    buffer = array('h', [0]) * total_frames
    fade_frames = max(1, int(sample_rate * 0.003))

    for start_beats, beats, note_name in events:
        freq = note_to_frequency(note_name)
        if not freq:
            continue

        start_frame = int(start_beats * seconds_per_beat * sample_rate)
        frames = max(1, int(beats * seconds_per_beat * sample_rate))
        amplitude = amplitude_for_note(note_name)
        phase = 0.0
        phase_step = freq / sample_rate

        for i in range(frames):
            phase += phase_step
            if phase >= 1.0:
                phase -= 1.0

            value = amplitude if phase < duty_cycle else -amplitude
            if i < fade_frames:
                value *= i / fade_frames
            else:
                tail = frames - i - 1
                if tail < fade_frames:
                    value *= max(tail, 0) / fade_frames

            idx = start_frame + i
            if idx >= len(buffer):
                break

            sample = buffer[idx] + int(value)
            if sample > 32767:
                sample = 32767
            elif sample < -32768:
                sample = -32768
            buffer[idx] = sample

    return buffer


def write_wave_file(path, samples, sample_rate):
    """Write PCM samples to a mono WAV file."""
    with wave.open(path, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(samples.tobytes())


class ChiptunePlayer:
    """Play the square-wave arrangement of 'O Christmas Tree' in a loop."""

    def __init__(self, bpm=CHIPTUNE_BPM, sample_rate=SAMPLE_RATE):
        self.bpm = bpm
        self.sample_rate = sample_rate
        self._audio_path = None
        self._track_duration = 0.0
        self._thread = None
        self._stop_event = threading.Event()
        self._process = None
        self._lock = threading.Lock()
        self._warned = False

    def start(self):
        """Render the track (if needed) and begin looping playback."""
        if self._thread and self._thread.is_alive():
            return

        self._stop_event.clear()
        if not self._audio_path:
            self._audio_path = self._render_audio()

        if not self._audio_path or not self._player_command():
            if not self._warned:
                print('⚠️  No supported CLI audio player found. Use --no-music to mute.')
                self._warned = True
            return

        self._thread = threading.Thread(target=self._play_loop, name='ChiptunePlayer', daemon=True)
        self._thread.start()

    def stop(self):
        """Stop playback and clean up temp files."""
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2)
        self._terminate_process()
        if self._audio_path:
            try:
                os.unlink(self._audio_path)
            except OSError:
                pass
            self._audio_path = None

    # Internal helpers ---------------------------------------------------------

    def _render_audio(self):
        samples = render_polyphonic_events(CHIPTUNE_EVENTS, self.bpm, self.sample_rate)
        self._track_duration = len(samples) / float(self.sample_rate)

        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        tmp_file.close()
        write_wave_file(tmp_file.name, samples, self.sample_rate)
        return tmp_file.name

    def _play_loop(self):
        while not self._stop_event.is_set():
            command = self._player_command()
            if not command:
                if not self._warned:
                    print('⚠️  Unable to play audio automatically on this system.')
                    self._warned = True
                return

            if command == 'winsound':
                try:
                    import winsound
                    winsound.PlaySound(self._audio_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                    # Wait for the track to finish or a stop request
                    self._stop_event.wait(self._track_duration)
                    winsound.PlaySound(None, winsound.SND_PURGE)
                except Exception:
                    if not self._warned:
                        print('⚠️  Windows audio playback failed; muting soundtrack.')
                        self._warned = True
                    return
            else:
                with self._lock:
                    self._process = subprocess.Popen(
                        command + [self._audio_path],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                self._process.wait()
                with self._lock:
                    self._process = None

    def _player_command(self):
        platform = sys.platform
        if platform.startswith('darwin') and shutil.which('afplay'):
            return ['afplay', '-q', '1']
        if platform.startswith('linux'):
            for cmd in ('aplay', 'paplay', 'ffplay'):
                binary = shutil.which(cmd)
                if not binary:
                    continue
                if cmd == 'ffplay':
                    return ['ffplay', '-nodisp', '-autoexit', '-loglevel', 'quiet']
                return [cmd]
        if os.name == 'nt':
            # winsound requires special handling, return sentinel
            return 'winsound'
        return None

    def _terminate_process(self):
        with self._lock:
            proc = self._process
            self._process = None
        if not proc:
            if os.name == 'nt':
                try:
                    import winsound
                    winsound.PlaySound(None, winsound.SND_PURGE)
                except Exception:
                    pass
            return

        if proc.poll() is None:
            try:
                proc.terminate()
                proc.wait(timeout=2)
            except Exception:
                proc.kill()

def draw_tree(blink_state, star_bright):
    """Draw the Christmas tree with ornaments and star"""
    
    # Get terminal width for centering
    try:
        terminal_width = shutil.get_terminal_size().columns
    except:
        terminal_width = 80  # Default if can't detect
    
    # Tree structure - each row has width and ornament positions
    tree_rows = [
        # (width, [ornament positions])
        (1, []),           # Star
        (3, [1]),          # Top tier
        (5, [1, 3]),
        (7, [2, 5]),       # Middle tier
        (9, [1, 4, 7]),
        (11, [2, 5, 8]),
        (13, [1, 6, 11]),  # Bottom tier
        (15, [3, 7, 12]),
        (17, [2, 8, 14]),
    ]
    
    trunk_rows = 2
    trunk_width = 1
    
    output = []
    
    # Calculate tree width for centering
    max_width = max(row[0] for row in tree_rows)
    
    # Extra padding to center the entire tree in the terminal
    left_margin = ' ' * max(0, (terminal_width - max_width) // 2)
    
    # Star
    star_color = Colors.YELLOW + Colors.BOLD if star_bright else Colors.YELLOW
    star = star_color + '★' + Colors.RESET
    padding = ' ' * ((max_width - 1) // 2)
    output.append(left_margin + padding + star)
    
    # Ornament colors to cycle through
    ornament_colors = [Colors.RED, Colors.BLUE, Colors.MAGENTA, Colors.CYAN, Colors.YELLOW]
    
    # Draw tree body
    for row_num, (width, ornament_positions) in enumerate(tree_rows[1:], 1):
        padding = ' ' * ((max_width - width) // 2)
        row = []
        
        for i in range(width):
            if i in ornament_positions:
                # Ornament - blink effect
                if blink_state and random.random() > 0.3:  # 70% chance to light up when blinking
                    color = random.choice(ornament_colors)
                    row.append(color + '●' + Colors.RESET)
                else:
                    row.append(Colors.GREEN + '●' + Colors.RESET)
            else:
                # Regular tree foliage
                row.append(Colors.GREEN + '*' + Colors.RESET)
        
        output.append(left_margin + padding + ''.join(row))
    
    # Trunk
    trunk_padding = ' ' * ((max_width - trunk_width) // 2)
    for _ in range(trunk_rows):
        output.append(left_margin + trunk_padding + Colors.YELLOW + '█' * trunk_width + Colors.RESET)
    
    # Add festive message
    output.append('')
    message = 'Merry Christmas!'
    msg_padding = ' ' * ((max_width - len(message)) // 2)
    output.append(left_margin + msg_padding + Colors.BOLD + Colors.RED + message + Colors.RESET)
    
    return '\n'.join(output)

def animate_tree(duration=30, fps=4):
    """
    Animate the Christmas tree
    
    Args:
        duration: How long to run animation (seconds)
        fps: Frames per second (higher = smoother but more CPU)
    """
    frame_delay = 1.0 / fps
    frames = int(duration * fps)
    
    for frame in range(frames):
        clear_screen()

        # Blink state changes every few frames
        blink_state = (frame // 2) % 2 == 0  # Toggle every 2 frames

        # Star pulse effect (slower than ornaments)
        star_bright = (frame // 4) % 2 == 0  # Toggle every 4 frames

        tree = draw_tree(blink_state, star_bright)
        print(tree)

        # Show frame counter (optional - remove for final video)
        print(f"\nFrame: {frame + 1}/{frames} | Press Ctrl+C to stop")

        time.sleep(frame_delay)

def should_play_music():
    """Determine whether the soundtrack should be enabled."""
    if os.environ.get(CHRISTMAS_TREE_NO_AUDIO):
        return False

    args = sys.argv[1:]
    if any(flag in args for flag in NO_MUSIC_FLAGS):
        # Remove the flag so it doesn't confuse other tooling
        sys.argv = [sys.argv[0]] + [a for a in args if a not in NO_MUSIC_FLAGS]
        return False

    return True


def main():
    """Main function"""
    clear_screen()
    print("Starting Christmas Tree Animation...")
    print("Press Ctrl+C to stop\n")
    time.sleep(2)

    music_player = None
    if should_play_music():
        music_player = ChiptunePlayer()
        music_player.start()

    try:
        # Run animation for 60 minutes at 4 FPS by default
        animate_tree(duration=60 * 60, fps=4)
    except KeyboardInterrupt:
        clear_screen()
        print("\n🎄 Thanks for watching! Happy Holidays! 🎄\n")
    finally:
        if music_player:
            music_player.stop()

if __name__ == "__main__":
    main()
