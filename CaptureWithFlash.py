import subprocess
import time
import pigpio
from gpiozero import MotionSensor, DistanceSensor, LED

# Initialize the pigpio instance
pi = pigpio.pi()

# Initialize the motion sensor
pir = MotionSensor(6)

# Initialize the ultrasonic sensor minimum recharge time is 0.5sec
ultrasonic = DistanceSensor(echo=4, trigger=5)

# Initialize the LED
led = LED(17)

# Initialize the GPIO pin for the flash
flash_pin = 18
pi.set_mode(flash_pin, pigpio.OUTPUT)

# Define function to take picture and trigger flash
def take_picture():
    while True:
        # Turn on the LED
        led.on()

        # Try to set the camera to auto focus
        try:
            subprocess.call(["gphoto2", "--set-config", "autofocusdrive=1"])
        except subprocess.CalledProcessError:
            print("Could not set autofocus mode")

        # Wait for the camera to achieve focus lock
        while True:
            try:
                focus_mode = subprocess.check_output(["gphoto2", "--get-config", "/main/capturesettings/afmode"]).decode('utf-8').split(" ")[-1].strip()
                if focus_mode == "Manual":
                    print("Camera set to manual focus")
                    break
                focus_lock = subprocess.check_output(["gphoto2", "--get-config", "/main/status/focusstatus"]).decode('utf-8').split(" ")[-1].strip()
                if focus_lock == "Locked":
                    print("Focus lock acquired")
                    break
            except subprocess.CalledProcessError:
                print("Could not get focus status")
            time.sleep(0.5)

        # Try to trigger the camera shutter
        try:
            subprocess.call(["gphoto2", "--trigger-capture"])
        except subprocess.CalledProcessError:
            print("Could not trigger camera shutter")

        # Wait for the camera to start exposure
        time.sleep(0.01)

        # Try to get the shutter speed
        try:
            shutter_speed = float(subprocess.check_output(["gphoto2", "--get-config", "/main/capturesettings/shutterspeed"]).decode('utf-8').split(" ")[-1])
        except (subprocess.CalledProcessError, ValueError):
            print("Could not get shutter speed")
            shutter_speed = 0

        if shutter_speed < 1/300:
            # Trigger the flash at the beginning of the exposure
            pi.write(flash_pin, 1)
            time.sleep(shutter_speed)
            pi.write(flash_pin, 0)
        else:
            # Trigger the flash near the end of the exposure
            time.sleep(shutter_speed * (299/300))
            pi.write(flash_pin, 1)
            time.sleep(shutter_speed * (1/300))
            pi.write(flash_pin, 0)

        # Turn off the LED
        led.off()

        # Wait for one second before taking the next picture
        time.sleep(1)

if __name__ == '__main__':
    # Call the take_picture function
    take_picture()

    # Clean up GPIO resources
    pir.close()
    ultrasonic.close()
    led.close()
    pi.stop()