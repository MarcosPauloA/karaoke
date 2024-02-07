import simpleaudio, time 

# Tempo in BPM
tempo = 180;

# calculate the delay in seconds between each click
delay = 60 / tempo

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
    time.sleep(delay)
   
# https://medium.com/@jackhuang.wz/building-a-metronome-in-python-c8e16826fe4f 