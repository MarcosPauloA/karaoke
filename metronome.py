import simpleaudio, time 
strong_beat = simpleaudio.WaveObject.from_wave_file('strong_beat.wav')
while True:
    strong_beat.play()
    time.sleep(0.5)
    
# https://medium.com/@jackhuang.wz/building-a-metronome-in-python-c8e16826fe4f 