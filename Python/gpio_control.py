from gpiozero import LED, Button, Buzzer
from time import sleep
from signal import pause

##led = LED(17)
button = Button(2)
buzzer = Buzzer(17)

##while True:
##    button.wait_for_press()
##    led.toggle()

##button.when_pressed = led.on
##button.when_released = led.off

##while True:
##    buzzer.on()
##    sleep(1)
##    buzzer.off()
##    sleep(1)

while True:
    buzzer.beep()

