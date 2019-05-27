#!/usr/bin/env python3

# Here we are going to import some libraries, so that we can re-use other people's code
import RPi.GPIO as GPIO
import time
import sys

# Possible IO Pins: 4, 17, 27, 22, 5, 6, 13, 19, 26, 18, 23, 24, 25, 12, 16, 20, 21

# Here we're just setting some collections and parameters that we will be using
# input_pins = (4, 27, 22, 5, 6, 13, 19, 26, 18, 23, 24, 25, 12, 16, 20, 21)
switch_input_detection_pin = 4
switch_output_pin = 17

# This is the functionality that will be carried out when the switch is opened and closed
def handle_switch_change_action(pin_number_that_changed):

    is_latch_closed = GPIO.input(pin_number_that_changed)
    GPIO.output(switch_output_pin, not is_latch_closed)

# Initialization of the GPIO pins
def setup_GPIO():

    # Here we're just doing pin setup, and declaring MOST of the pins as INPUTS
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(switch_input_detection_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # This is where we connect the callback to the state-change event
    GPIO.add_event_detect(switch_input_detection_pin,
                          GPIO.BOTH,
                          callback=handle_switch_change_action)

    # Here we declare one pin as an output.
    GPIO.setup(switch_output_pin, GPIO.OUT, initial=0)
    handle_switch_change_action(switch_input_detection_pin)

# The first method that is called, which calls everything else...
def main():
    try:
        print("{} running".format(sys.argv[0]))
        setup_GPIO()
        time.sleep(1)
        print("now fully set up and looping")
        # Here we are just going to keep the program running. We can declare the sleep-time
        # to be as long as we want; the callback function isn't dependant on this being "awake"
        while True:
            time.sleep(20)
    except KeyboardInterrupt:
        pass
    finally:
        # A bit of house-keeping when we shut-down to make sure we're not bad citizens
        GPIO.cleanup()

# This is where "Main" is actually called...
if __name__ == "__main__":
    main()