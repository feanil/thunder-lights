from pyaudio import PyAudio, paInt16
from thunderDetector import ThunderDetector
from serial import Serial
from glob import glob
import random

pa = PyAudio()
info = pa.get_host_api_info_by_index(0)

numdevices = info.get('deviceCount')
for i in range(0, numdevices):
    if (pa.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print "Input Device id ", i, " - ", pa.get_device_info_by_host_api_device_index(0, i).get('name')

chunk = 1024
on_threshold = 17
off_threshold = 10
counter = 0
time_constant = 0.1

detector = ThunderDetector(chunk)


stream = pa.open(format = paInt16,
                 channels = 2,
                 rate = 44100,
                 input=True,
                 )

data=stream.read(chunk)

serial_device_names = glob("/dev/ttyUSB*") + glob("/dev/ttyACM*")
serial_devices = [ Serial(device_name, baudrate=115200) for device_name in serial_device_names ]

while data:
    #check if there is thunder in the data
    detector.detect(data, on_threshold, off_threshold, time_constant)
    #get new data
    data=stream.read(chunk)
    #change this print statement to output
    intensity = int(detector.intensity)

    # Switch which devices to output to everytime it's quiet
    if intensity > 0:
        print intensity
        if serial_devices:
            random.shuffle(serial_devices)

    # Write data to relevant serial devices.
    print "Intensity: {}".format(intensity)
    print "Serial Device Names: {}".format(serial_device_names)
    for device in serial_devices:
        device.write([intensity])

stream.stop_stream()
stream.close()
for device in serial_devices:
    device.close()
pa.terminate()

