#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import sys

def setup_GPIO():
    pass

# The first method that is called, which calls everything else...
def main():
    try:
        filename = sys.argv[0]
        print("{} is running".format(filename))
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