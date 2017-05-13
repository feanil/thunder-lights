from pyaudio import PyAudio, paInt16
from thunderDetector import ThunderDetector

pa = PyAudio()

chunk = 1024
threshold = 100
counter=0

detector = ThunderDetector(chunk)


stream = pa.open(format = paInt16,
                 channels = 1,
                 rate = 44100,
                 input=True)

data=stream.read(chunk)

while len(data)>0:
    #check if there is thunder in the data
    detector.detect(data, 100)
    #get new data
    data=stream.read(chunk)
    #change this print statement to output
    print detector.intensity

stream.stop_stream()
stream.close()
pa.terminate()

