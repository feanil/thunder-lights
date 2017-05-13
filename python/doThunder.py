from pyaudio import PyAudio, paInt16
from thunderDetector import ThunderDetector
from serial import Serial

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

ser = Serial('/dev/ttyUSB0')

while len(data)>0:
    #check if there is thunder in the data
    detector.detect(data, 100)
    #get new data
    data=stream.read(chunk)
    #change this print statement to output
    intensity = int(detector.intensity)
    print intensity
    ser.write([0,intensity])

stream.stop_stream()
stream.close()
ser.close()
pa.terminate()

