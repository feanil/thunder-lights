from __future__ import print_function
import click
import serial
import time

def update_lights(intensity):
    ser = serial.Serial('/dev/ttyUSB0')
    ser.write(intensity)
    ser.close()
    print("Serial Written {}.".format(intensity))

@click.command()
@click.option('--intensity', prompt='What Intensity?',
        help='Intensity of the lightning.',
        type=int)
def main(intensity):
    print(update_lights(intensity))

if __name__ == "__main__":
#    main()
    while True:
        for i in range(50,2210):
            update_lights(i)
            time.sleep(1)
