from gpiozero import Button, LED, Buzzer
from time import sleep

button = Button(21)
red = LED(23)
yellow = LED(22)
green = LED(24)
buzzer = Buzzer(18)

def ped_xing():
    buzzer.beep(.2, 1, 10, False)
    sleep(3)

def go_red():
    buzzer.beep(1, 2)
    yellow.on()
    green.off()
    sleep(5)
    red.on()
    yellow.off()
    ped_xing()

def go_green():
    red.off()
    green.on()

def main():
    while True:
        go_green()
        button.wait_for_press()
        sleep(2)
        go_red()
main()
