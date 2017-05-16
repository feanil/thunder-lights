from pyaudio import PyAudio, paInt16
from thunderDetector import ThunderDetector
from serial import Serial

pa = PyAudio()
info = pa.get_host_api_info_by_index(0)

numdevices = info.get('deviceCount')
for i in range(0, numdevices):
        if (pa.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print "Input Device id ", i, " - ", pa.get_device_info_by_host_api_device_index(0, i).get('name')

chunk = 1024
on_threshold = 4
off_threshold = 2
counter=0

detector = ThunderDetector(chunk)


stream = pa.open(format = paInt16,
                 channels = 5,
                 rate = 44100,
                 input=True,
                 )

data=stream.read(chunk)

ser = None
#ser = Serial('/dev/ttyUSB2')

while len(data)>0:
    #check if there is thunder in the data
    detector.detect(data, on_threshold, off_threshold)
    #get new data
    data=stream.read(chunk)
    #change this print statement to output
    intensity = int(detector.intensity)
    print intensity
    if ser:
        ser.write([intensity])

stream.stop_stream()
stream.close()
if ser:
    ser.close()
pa.terminate()

