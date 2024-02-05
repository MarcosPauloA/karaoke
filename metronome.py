import simpleaudio, time 
strongBeat = simpleaudio.WaveObject.from_wave_file('strong_beat.wav')
weakBeat = simpleaudio.WaveObject.from_wave_file('weak_beat.wav')
count = 0
while True:
    count += 1
    if count == 1:
        strongBeat.play()
    else:
        weakBeat.play()
    if count == 4:
        count = 0
    time.sleep(0.5)
    
# https://medium.com/@jackhuang.wz/building-a-metronome-in-python-c8e16826fe4f 