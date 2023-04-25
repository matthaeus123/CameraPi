import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)  # set up GPIO pin 4 as an output for the signal to the transistor base

try:
    while True:
        GPIO.output(4, GPIO.HIGH)
        time.sleep(0.1)  # adjust this delay as necessary for your camera
        GPIO.output(4, GPIO.LOW)
        time.sleep(0.1)  # adjust this delay as necessary for your camera

        # Trigger the camera by applying a signal to the base of the transistor on GPIO pin 4
        GPIO.output(4, GPIO.HIGH)
        time.sleep(0.1)  # adjust this delay as necessary for your camera
        GPIO.output(4, GPIO.LOW)
        time.sleep(5)  # adjust this delay as necessary for your camera

except KeyboardInterrupt:
    # Clean up GPIO pin 4 and exit gracefully on Ctrl+C
    GPIO.cleanup(4)
