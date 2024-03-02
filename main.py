matrix = [['e'],['B'],['G'],['D'],['A'],['E']]

# Maps the fretNumber with their note, each dictionary is representing a guitar string and the number is the fretNumber
fretNoteMapping = [{},{},{0:"G3",1:"Ab3",2:"A3",3:"Bb3"},{},{},{}]

# Maps the strings notes with their frequencies in Hz using a list of dictionaries
noteMapping = [{"E4":329.63},{},{"G3":196,"Ab3":207.65,"A3":220,"Bb3":233.08},{},{},{}]

def getNoteFrequency(noteString, noteFretNumb):
    note = fretNoteMapping[noteString-1][noteFretNumb]
    noteFreq = noteMapping[noteString-1][note]
    return noteFreq

def comparesFrequency(voiceFrequency, noteFrequency):
    # Tolerance of frequency discrepancy 
    tolerance = 6.5
    
    if (voiceFrequency > noteFrequency - tolerance) and (voiceFrequency < noteFrequency + tolerance):
        print("You hit the note!")
    elif voiceFrequency > noteFrequency:
        print("Too High")
        print("You're Freq: ", voiceFrequency, " Note Freq: ", noteFrequency)
    else:
        print("Too Low")
        print("You're Freq: ", voiceFrequency, " Note Freq: ", noteFrequency)
import guitarpro
def singSong(pitch):
    song = guitarpro.parse('Nirvana.gp4')
    track = song.tracks[0]
    measure = track.measures[1]
    for voice in measure.voices:
        for beat in voice.beats:
            for note in beat.notes: 
                matrix[note.string-1].append(note.value)
                noteFreq = getNoteFrequency(note.string, note.value)
                comparesFrequency(pitch, noteFreq)
                return noteFreq



'''   
for string in matrix:
    for char in string:
        print(char, end='')
    print()

import tkinter as tk

# Create a simple GUI window
root = tk.Tk()
root.title("My First GUI")

# Add a label widget
label = tk.Label(root, text=song.title)
label.pack()

# Add a label widget
label = tk.Label(root, text=song.artist)
label.pack()
root.geometry("500x200")
# Add a label widget
#label = tk.Label(root, background="blue", borderwidth=1080)
#label.pack()

# Run the event loop
root.mainloop()


The song object contains all the information about the GP file, such as tracks, measures, beats, notes, effects, etc. You can access and modify these attributes using the PyGuitarPro API2.

For example, to transpose a track by one semitone, you can do:

Python

track = song.tracks[0] # get the first track
track.transpose(1) # transpose by one semitone
Código gerado por IA. Examine e use com cuidado. Mais informações em perguntas frequentes.
To write the modified song to a new GP file, you can do:

Python

guitarpro.write(song, 'test_transposed.gp5')
https://github.com/Perlence/PyGuitarPro/tree/master
'''
