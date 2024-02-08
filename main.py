matrix = [['e'],['B'],['G'],['D'],['A'],['E']]

import guitarpro
song = guitarpro.parse('Nirvana.gp4')
track = song.tracks[0]
measure = track.measures[0];
voice = measure.voices[0];
for beat in voice.beats:
    for note in beat.notes:
        matrix[note.string-1].append(note.value)
print(matrix)
'''
for measure in track.measures:
    for voice in measure.voices:
        for beat in voice.beats:
            for note in beat.notes:
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
