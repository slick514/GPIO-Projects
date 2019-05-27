#!/usr/bin/env python3

# The first line will make your IDE complain, unless you are somehow running directly on a Raspberry Pi
import RPi.GPIO as GPIO
import time
import sys


# If a resistor and LED are connected correctly between pin-4 (BCM) and ground, this program should cause the LED to
# turn on for 1 second.


# The following has nothing to do with this particular program, and is just here for easy Raspberry Pi reference;
# Possible GPIO Pins (Broadcom SOC Channel Numbering) for the Raspberry Pi:
# 4, 17, 27, 22, 5, 6, 13, 19, 26, 18, 23, 24, 25, 12, 16, 20, 21


# We are using pin-4 (GPIO Broadcom numbering) as our output
output_pin = 4


# Print the name of the script that is running to standard output...
def print_filename():
    filename = sys.argv[0]
    print("{} is running".format(filename))


# Initialization of the GPIO pin(s)
def setup_GPIO():

    # We are going to refer to the pins by the Broadcom SOC channel numbering.
    GPIO.setmode(GPIO.BCM)

    # Output pin setup
    GPIO.setup(output_pin, GPIO.OUT, initial=0)
    time.sleep(1) # who knows how long things take to set up.  We'll wait a second and let things finish.


# Turn the output on, then off
def do_1s_output():
    GPIO.output(output_pin, 1)
    time.sleep(1)
    GPIO.output(output_pin, 0)


# The first method that will be called
def main():
    try:
        print_filename()
        setup_GPIO()
        do_1s_output()

    except KeyboardInterrupt:
        pass
    finally:
        # A bit of house-keeping when we shut-down to make sure we're not bad citizens
        GPIO.cleanup()


# This is where "Main" is actually called...
if __name__ == "__main__":
    main()