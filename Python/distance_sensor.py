from gpiozero import DistanceSensor

def hello():
    print("Hello")

def bye():
    print("Bye")

ultrasonic = DistanceSensor(echo=21, trigger=16, threshold_distance=.5)

ultrasonic.when_in_range = hello
ultrasonic.when_out_of_range = bye
