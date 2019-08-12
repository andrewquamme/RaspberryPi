import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

for i in range(1,11):
    print(i)
    GPIO.output(18, True)
    time.sleep(1/i)
    GPIO.output(18, False)
    time.sleep(1)

            
