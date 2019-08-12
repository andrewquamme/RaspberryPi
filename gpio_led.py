from gpiozero import LED
from time import sleep

led = LED(18)

def blink(pattern):
    for c in pattern:
        if c == '.':
            led.on()
            sleep(.1)
            led.off()
        elif c == '-':
            led.on()
            sleep(.5)
            led.off()
        elif c == ' ':
            sleep(1)
        sleep(.5)

blink("... --- ...")
            
