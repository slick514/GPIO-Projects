#!/usr/bin/env python3

# The first line will make your IDE complain, unless you are somehow running directly on a Raspberry Pi
import RPi.GPIO as GPIO
import time
import sys


# Possible GPIO Pins (Broadcom SOC Channel Numbering) for the Raspberry Pi:
# 4, 17, 27, 22, 5, 6, 13, 19, 26, 18, 23, 24, 25, 12, 16, 20, 21

# Here we're just setting some collections and parameters that we will be using
input_detection_pin = 4
output_pin = 17
wakeup_period_s = 60 # we'll wake up every minute...


# This is the functionality that will be carried out when the switch is opened and closed
def cb_on_input_change(changed_pin):

    is_latch_closed = GPIO.input(changed_pin)

    # If uncommented, the following line will set the output as the opposite of the input
    # GPIO.output(output_pin, not is_latch_closed)

    # If uncommented, the following line will set the output as the same as the input
    GPIO.output(output_pin, is_latch_closed)


# Initialization of the GPIO pins
def setup_GPIO():

    # We are going to refer to the pins by the Broadcom SOC channel numbering.
    GPIO.setmode(GPIO.BCM)

    # Input pin set-up
    # I have not yet figured out how to get the pull-up/pull-down to work in software, but I try here anyway
    GPIO.setup(input_detection_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # Declaring the name of the function that will be called when the state of the input changes;
    # This will detect both rising-edge and falling-edge events (GPIO.BOTH)
    GPIO.add_event_detect(input_detection_pin,
                          GPIO.BOTH,
                          callback=cb_on_input_change)

    # Output pin setup
    GPIO.setup(output_pin, GPIO.OUT, initial=0)

    # Calling the callback function once, to initialize the input/output relationship prior to an input event
    cb_on_input_change(input_detection_pin)


# The first method that will be called
def main():
    try:
        filename = sys.argv[0]

        # Print out the name of the script that is running...
        print("{} is running".format(filename))

        setup_GPIO()

        # This loop just keeps the program running. The callback functionality isn't dependant on things being "awake"
        while True:
            time.sleep(wakeup_period_s)
    except KeyboardInterrupt:
        pass
    finally:
        # A bit of house-keeping when we shut-down to make sure we're not bad citizens
        GPIO.cleanup()


# This is where "Main" is actually called...
if __name__ == "__main__":
    main()