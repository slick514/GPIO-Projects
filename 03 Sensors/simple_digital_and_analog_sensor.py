#!/usr/bin/env python3

# The first line will make your IDE complain, unless you are somehow running directly on a Raspberry Pi
import RPi.GPIO as GPIO
import time
import sys


# Kind of a "default/starter"-script for handling the logic from a variety of sensors that output a "HIGH/LOW"
# digital output.


# The following has nothing to do with this particular program, and is just here for easy Raspberry Pi reference;
# Possible GPIO Pins (Broadcom SOC Channel Numbering) for the Raspberry Pi:
# 4, 17, 27, 22, 5, 6, 13, 19, 26, 18, 23, 24, 25, 12, 16, 20, 21

# Declaration of pins (BCM-numbering) that we will use for the GPIO inputs and outputs
digital_detection_input__pin = 27
digital_detection_output_pin = 22

# A lot of these sensors have analog outputs as well.  I'm not sure how often they are encountered, and the Pi
# inputs are rather strictly digital, but there are some work-arounds that I would like to try out, where we
# might be able to use a resistor/capacitor setup to rig an analog input... we'll see
analog_detection_input__pin = 5
analog_detection_output_pin = 6

# Pairing up the inputs with their respective outputs, using a dictionary
IO_pairs = {analog_detection_input__pin: analog_detection_output_pin,
            digital_detection_input__pin: digital_detection_output_pin}

# Wake up every minute...
wakeup_period_s = 60


# Print out the name of the script that is running...
def print_filename():
    filename = sys.argv[0]
    print("{} is running".format(filename))


# This is the functionality that will be carried out when the state of one of the inputs changes
# In this case, we're going to output the opposite of whatever we are reading on the input.
def cb_on_input_change(changed_pin):

    # This assumes that the sensor returns a logical-high normally, and 0V when tripped.
    # An example of this is the YL-83 Rain Sensor.
    sensor_state = not GPIO.input(pin_number_that_changed)
    GPIO.output(IO_pairs[pin_number_that_changed], sensor_state)


# Initialization of the GPIO pins
def initialize_GPIO():

    # Setup all the inputs and outputs
    GPIO.setmode(GPIO.BCM)
    for key, value in IO_pairs.items():
        GPIO.setup(key, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(value, GPIO.OUT, initial=0)


def declare_GPIO_functionality():
    for key in IO_pairs.keys():
        GPIO.add_event_detect(key,
                          GPIO.BOTH,
                          callback=cb_on_input_change)
        handle_switch_change_action(key)


# The first method that is called, which calls everything else...
def main():
    try:
        print_filename()
        initialize_GPIO()
        declare_GPIO_functionality()

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