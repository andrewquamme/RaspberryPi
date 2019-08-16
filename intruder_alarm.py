from gpiozero import MotionSensor, LED, Buzzer

pir = MotionSensor(21)
alarm = Buzzer(6)
led = LED(23)

while True:
    pir.wait_for_motion()
    print("Someone is in the area!")
    led.on()
    alarm.blink(.1, .1, 3)
    pir.wait_for_no_motion()
    led.off()
