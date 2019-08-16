from gpiozero import MotionSensor

pir = MotionSensor(21)

while True:
    pir.wait_for_motion()
    print("Someone is in the area!")
    pir.wait_for_no_motion()
