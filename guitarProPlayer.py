import guitarpro
from mido import Message, MidiFile, MidiTrack, MetaMessage
import pygame
import math

# --- Config ---
INPUT_FILE = "Nirvana.gp4"
OUTPUT_MIDI = "output.mid"
TICKS_PER_BEAT = 480  # MIDI standard
TRACK_KEYWORDS = ["guitar"]  # Only include tracks with these words in their name (case-insensitive)
DEFAULT_TEMPO_BPM = 120
DEFAULT_TEMPO_MICROSECONDS = 60000000 // DEFAULT_TEMPO_BPM


fretNoteMapping = [
    # 6th string E2
    {
        0:"E2", 1:"F2", 2:"F#2", 3:"G2", 4:"G#2", 5:"A2", 6:"A#2", 7:"B2", 8:"C3", 9:"C#3", 10:"D3", 11:"D#3", 12:"E3"
    },
    # 5th string A2
    {
        0:"A2", 1:"A#2", 2:"B2", 3:"C3", 4:"C#3", 5:"D3", 6:"D#3", 7:"E3", 8:"F3", 9:"F#3", 10:"G3", 11:"G#3", 12:"A3"
    },
    # 4th string D3
    {
        0:"D3", 1:"D#3", 2:"E3", 3:"F3", 4:"F#3", 5:"G3", 6:"G#3", 7:"A3", 8:"A#3", 9:"B3", 10:"C4", 11:"C#4", 12:"D4"
    },
    # 3rd string G3
    {
        0:"G3", 1:"G#3", 2:"A3", 3:"A#3", 4:"B3", 5:"C4", 6:"C#4", 7:"D4", 8:"D#4", 9:"E4", 10:"F4", 11:"F#4", 12:"G4"
    },
    # 2nd string B3
    {
        0:"B3", 1:"C4", 2:"C#4", 3:"D4", 4:"D#4", 5:"E4", 6:"F4", 7:"F#4", 8:"G4", 9:"G#4", 10:"A4", 11:"A#4", 12:"B4"
    },
    # 1st string E4
    {
        0:"E4", 1:"F4", 2:"F#4", 3:"G4", 4:"G#4", 5:"A4", 6:"A#4", 7:"B4", 8:"C5", 9:"C#5", 10:"D5", 11:"D#5", 12:"E5"
    }
]


noteMapping = {
    "E2": 82.41, "F2": 87.31, "F#2": 92.50, "G2": 98.00, "G#2": 103.83, "A2": 110.00, "A#2": 116.54, "B2": 123.47,
    "C3": 130.81, "C#3": 138.59, "D3": 146.83, "D#3": 155.56, "E3": 164.81, "F3": 174.61, "F#3": 185.00, "G3": 196.00,
    "G#3": 207.65, "A3": 220.00, "A#3": 233.08, "B3": 246.94, "C4": 261.63, "C#4": 277.18, "D4": 293.66, "D#4": 311.13,
    "E4": 329.63, "F4": 349.23, "F#4": 369.99, "G4": 392.00, "G#4": 415.30, "A4": 440.00, "A#4": 466.16, "B4": 493.88,
    "C5": 523.25, "C#5": 554.37, "D5": 587.33, "D#5": 622.25, "E5": 659.25
}

# Optional: map GP drum notes to General MIDI drum notes
DRUM_MAP = {
    35: 36,  # Acoustic Bass Drum → Bass Drum 1
    38: 38,  # Snare Drum
    40: 40,  # Electric Snare
    42: 42,  # Closed Hi-Hat
    46: 46,  # Open Hi-Hat
    49: 49,  # Crash Cymbal
    51: 51,  # Ride Cymbal
}

# --- Load GP4 File ---
song = guitarpro.parse(INPUT_FILE)
gp_ticks_per_quarter = 960  # fixed

# Convert GP tempo to microseconds per beat (for MIDI)
tempo_bpm = song.tempo or 120
DEFAULT_TEMPO_MICROSECONDS = 60000000 // tempo_bpm

# --- Create MIDI File ---
mid = MidiFile(ticks_per_beat=TICKS_PER_BEAT)

# --- Tempo Track ---
tempo_track = MidiTrack()
tempo_track.append(MetaMessage('set_tempo', tempo=DEFAULT_TEMPO_MICROSECONDS, time=0))
mid.tracks.append(tempo_track)

# --- Track Conversion ---
for gp_track in song.tracks:
    # Skip tracks that don't match filter keywords
    name = gp_track.name.lower()
    if not any(keyword in name for keyword in TRACK_KEYWORDS):
        continue

    if not gp_track.measures:
        continue

    midi_track = MidiTrack()
    mid.tracks.append(midi_track)

    track_name = gp_track.name
    channel = 9 if gp_track.isPercussionTrack else 0
    instrument = gp_track.channel.instrument if not gp_track.isPercussionTrack else 0

    midi_track.append(MetaMessage('track_name', name=track_name, time=0))
    if not gp_track.isPercussionTrack:
        midi_track.append(Message('program_change', program=instrument, channel=channel, time=0))

    current_time = 0

    for measure in gp_track.measures:
        for voice in measure.voices:
            for beat in voice.beats:
                if not beat.notes:
                    current_time += int((beat.duration.time / gp_ticks_per_quarter) * TICKS_PER_BEAT)
                    continue

                duration_ticks = int((beat.duration.time / gp_ticks_per_quarter) * TICKS_PER_BEAT) or 120

                for note in beat.notes:
                    mapNote = fretNoteMapping[note.string-1][note.value]
                    frequency = noteMapping[mapNote] 
                    # Convert frequency to MIDI note number
                    pitch = int(round(69 + 12 * (math.log2(frequency / 440.0))))
                    # pitch = note.value

                    if gp_track.isPercussionTrack:
                        pitch = DRUM_MAP.get(pitch, 38)
                    else:
                        pitch += 12

                    velocity = 100
                    midi_track.append(Message('note_on', note=pitch, velocity=velocity, time=current_time, channel=channel))
                    midi_track.append(Message('note_off', note=pitch, velocity=velocity, time=duration_ticks, channel=channel))
                    current_time = 0
                current_time = duration_ticks

# --- Save MIDI File ---
mid.save(OUTPUT_MIDI)
print(f"Saved MIDI file: {OUTPUT_MIDI}")

# --- Play MIDI File ---
pygame.init()
pygame.mixer.init()

print("Playing MIDI file...")
pygame.mixer.music.load(OUTPUT_MIDI)
pygame.mixer.music.play()

# Wait for playback to finish
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
