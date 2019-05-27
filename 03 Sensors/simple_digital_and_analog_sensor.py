#!/usr/bin/env python3

# Here we are going to import some libraries, so that we can re-use other people's code
import RPi.GPIO as GPIO
import time
import sys

# Possible IO Pins: 4, 17, 27, 22, 5, 6, 13, 19, 26, 18, 23, 24, 25, 12, 16, 20, 21

# Here we're just setting parameters that we will be using
digital_detection_input__pin = 27
digital_detection_output_pin = 22

analog_detection_input__pin = 5
analog_detection_output_pin = 6

IO_pairs = {analog_detection_input__pin:analog_detection_output_pin,
            digital_detection_input__pin:digital_detection_output_pin}

# This is the functionality that will be carried out when the switch is opened and closed
def handle_switch_change_action(pin_number_that_changed):

    is_sensor_on = not GPIO.input(pin_number_that_changed)
    GPIO.output(IO_pairs[pin_number_that_changed], is_sensor_on)

# Initialization of the GPIO pins
def setup_GPIO():

    # Here we're just doing pin setup
    GPIO.setmode(GPIO.BCM)
    for key, value in IO_pairs.items():
        GPIO.setup(key, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # This is where we connect the callback to the state-change event
        GPIO.add_event_detect(key,
                          GPIO.BOTH,
                          callback=handle_switch_change_action)

        # Here we declare the corresponding output for each input.
        GPIO.setup(value, GPIO.OUT, initial=0)
        handle_switch_change_action(key)


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