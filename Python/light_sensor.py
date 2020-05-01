from gpiozero import LightSensor, Buzzer

ldr = LightSensor(19)
while True:
    print(ldr.value)
