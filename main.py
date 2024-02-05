import guitarpro
song = guitarpro.parse('Nirvana.gp4')

print(song.tempo);

'''
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